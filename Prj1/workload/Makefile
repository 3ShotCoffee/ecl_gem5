# Copyright (c) 2022 The Regents of the University of California
# All Rights Reserved.
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

GEM5_PATH = /root/gem5
ISA = x86

.DEFAULT_GOAL := matmul-base

all: matmul-base matmul-blocked matmul-blocked-full

matmul-base:
	gcc -O2 -o ../matmul-base matmul-base.c \
	-I$(GEM5_PATH)/include \
	-L$(GEM5_PATH)/util/m5/build/$(ISA)/out \
	-lm5

matmul-blocked:
	gcc -O2 -o ../matmul-blocked matmul-blocked.c \
	-I$(GEM5_PATH)/include \
	-L$(GEM5_PATH)/util/m5/build/$(ISA)/out \
	-lm5
	
matmul-oblivious:
	gcc -O2 -o ../matmul-oblivious matmul-oblivious.c \
	-I$(GEM5_PATH)/include \
	-L$(GEM5_PATH)/util/m5/build/$(ISA)/out \
	-lm5

matmul-morton:
	gcc -O2 -o ../matmul-morton matmul-morton.c \
	-I$(GEM5_PATH)/include \
	-L$(GEM5_PATH)/util/m5/build/$(ISA)/out \
	-lm5

clean:
	- rm matmul-base
	- rm matmul-blocked
	- rm matmul-blocked-full
