# Copyright (c) 2015 Jason Power
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

""" This file creates a single CPU and a two-level cache system.
This script takes a single parameter which specifies a binary to execute.
If none is provided it executes 'hello' by default (mostly used for testing)

See Part 1, Chapter 3: Adding cache to the configuration script in the
learning_gem5 book for more information about this script.
This file exports options for the L1 I/D and L2 cache sizes.

IMPORTANT: If you modify this file, it's likely that the Learning gem5 book
           also needs to be updated. For now, email Jason <power.jg@gmail.com>

"""

# import the m5 (gem5) library created when gem5 is built
import m5

# import all of the SimObjects
from m5.objects import *

m5.util.addToPath("../configs/")

# import the caches which we made
from caches_l1 import *

# import the SimpleOpts module
from common import SimpleOpts

import math

# Default to running the m5ops version of x86-matrix-multiply from gem5-resources.
default_binary = "/home/jhpark/gem5/Prj1/matmul-blocked"

num_channels = 4  # Number of DRAM channels
total_mem_size = 512 * 1024 * 1024  # 512MB
channel_size = total_mem_size // num_channels

# Binary to execute
SimpleOpts.add_option(
    "num_channels",
    nargs="?",
    type=int,
    default=4,
    help="Number of DRAM channels.",
)

# Binary to execute
SimpleOpts.add_option(
    "binary",
    nargs="?",
    default=default_binary,
    help="Path to the binary to run.",
)

# Command-line arguments for the binary
SimpleOpts.add_option(
    "bin_args",
    nargs=SimpleOpts.REMAINDER,
    default=[],
    help="Arguments to pass to the binary.",
)

# Finalize the arguments and grab the args so we can pass it on to our objects
args = SimpleOpts.parse_args()

# create the system we are going to simulate
system = System()

# Set the clock frequency of the system (and all of its children)
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()

# Set up the system
system.mem_mode = "timing"  # Use timing accesses
system.mem_ranges = [AddrRange("512MB")]  # Create an address range

# Create a simple CPU
system.cpu = X86TimingSimpleCPU()
system.cpu.clk_domain = SrcClockDomain()
system.cpu.clk_domain.clock = "1THz"
system.cpu.clk_domain.voltage_domain = system.clk_domain.voltage_domain

# Create an L1 instruction and data cach
system.cpu.icache = L1ICache(args)
system.cpu.dcache = L1DCache(args)

# Connect the instruction and data caches to the CPU
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

# Create a memory bus
system.membus = SystemXBar()

# Hook the CPU ports up to the membus
system.cpu.icache.connectBus(system.membus)
system.cpu.dcache.connectBus(system.membus)

# create the interrupt controller for the CPU
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

# Connect the system up to the membus
system.system_port = system.membus.cpu_side_ports

# Create a multi-channel DDR5 memory configuration
interleave_bits = int(math.ceil(math.log2(args.num_channels)))
interleave_size = 64  # bytes (should match burst size)
total_mem_size = 512 * 1024 * 1024  # 512MB

for i in range(args.num_channels):
    mem_ctrl = MemCtrl()
    mem_ctrl.dram = DDR5_6400_4x8()
    mem_ctrl.dram.range = AddrRange(
        start=0,
        size=total_mem_size,
        intlvHighBit=int(math.log2(interleave_size)) + interleave_bits - 1,
        intlvBits=interleave_bits,
        intlvMatch=i,
    )
    mem_ctrl.port = system.membus.mem_side_ports
    setattr(system, f"mem_ctrl_{i}", mem_ctrl)  # <- registers with SimObject hierarchy

system.workload = SEWorkload.init_compatible(args.binary)

# Create a process for a simple matrix-multiply application
process = Process()
# Set the command
# cmd is a list which begins with the executable (like argv)
process.cmd = [args.binary] + args.bin_args
# Set the cpu to use the process as its workload and create thread contexts
system.cpu.workload = process
system.cpu.createThreads()

# set up the root SimObject and start the simulation
root = Root(full_system=False, system=system)
# instantiate all of the objects we've created above
m5.instantiate()

print("Beginning simulation!")
exit_event = m5.simulate()

print("Exiting @ tick %i because %s" % (m5.curTick(), exit_event.getCause()))
