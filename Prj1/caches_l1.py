# -*- coding: utf-8 -*-
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

""" Revision of the file configs/learning_gem5/part1/caches.py with only l1 caches.

This file contains L1 I/D caches to be used in the simple
gem5 configuration script. It uses the SimpleOpts wrapper to set up command
line options from each individual class.
"""

import m5
from m5.objects import Cache, WriteAllocator

# Add the common scripts at configs/ to our path
m5.util.addToPath("../configs/")

from common import SimpleOpts

from m5.objects.ReplacementPolicies import *
from m5.objects.Prefetcher import *

# Some specific options for caches
# For all options see src/mem/cache/BaseCache.py

class L1Cache(Cache):
    """Simple L1 Cache with default values"""

    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20

    def __init__(self, options=None):
        super(L1Cache, self).__init__()
        pass

    def connectBus(self, bus):
        """Connect this cache to a memory-side bus"""
        self.mem_side = bus.cpu_side_ports

    def connectCPU(self, cpu):
        """Connect this cache's port to a CPU-side port
        This must be defined in a subclass"""
        raise NotImplementedError


class L1ICache(L1Cache):
    """Simple L1 instruction cache with default values"""

    assoc = 2

    # Set the default size
    size = "16kB"

    SimpleOpts.add_option(
        "--l1i_size", help=f"L1 instruction cache size. Default: {size}"
    )

    def __init__(self, opts=None):
        super(L1ICache, self).__init__(opts)
        if not opts or not opts.l1i_size:
            return
        self.size = opts.l1i_size

    def connectCPU(self, cpu):
        """Connect this cache's port to a CPU icache port"""
        self.cpu_side = cpu.icache_port


class L1DCache(L1Cache):
    """Simple L1 data cache with default values"""

    # Set the default configuration
    assoc = 2
    size = "64kB"
    replacement_policy = LRURP()

    SimpleOpts.add_option(
        "--l1d_size", help=f"L1 data cache size. Default: {size}"
    )

    SimpleOpts.add_option(
        "--l1d_assoc", help=f"L1 data cache associativity. Default: {assoc}"
    )

    SimpleOpts.add_option(
        "--l1d_rp", help="L1D replacement policy: LRU, Random, FIFO, LFU, etc. Default: LRU"
    )

    def __init__(self, opts=None):
        super(L1DCache, self).__init__(opts)
        if not opts: # ensures no AttributeError
            return
        if opts.l1d_size:
            self.size = opts.l1d_size
        if opts.l1d_assoc:
            self.assoc = opts.l1d_assoc
        if opts.l1d_rp:
            self.replacement_policy = self._parse_rp(opts.l1d_rp)

    def connectCPU(self, cpu):
        """Connect this cache's port to a CPU dcache port"""
        self.cpu_side = cpu.dcache_port

    # -- Helper functions to parse the command line options --

    def _parse_rp(self, name):
        """Parse the replacement policy name and return the corresponding object"""
        rp_map = {
            'FIFO' : FIFORP(), 
            'SecondChance' : SecondChanceRP(), 
            'LFU' : LFURP(), 
            'LRU' : LRURP(), 
            'MRU' : MRURP(), 
            'Random ': RandomRP(),
        }
        return rp_map.get(name, LRURP())  # default to LRU if unknown
