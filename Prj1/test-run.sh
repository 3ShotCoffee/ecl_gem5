#!/bin/bash

../build/X86/gem5.opt --outdir=l1_test_100 system_l1.py \
--l1d_size=32kB \
--l1d_assoc=4 \
--l1d_rp=FIFO \
matmul-base 100