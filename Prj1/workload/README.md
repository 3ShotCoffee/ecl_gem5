# workload/
A directory for workload source files and Makefile

## Overview
* matmul-original : the original matrix multiplication benchmark from *gem5 resources*. Only for reference.
* matmul-base : basic matrix multiplcation with no tiling.
* matmul-blocked : matrix multiplication with tiling.
* matmul-oblivious : cache-oblivious matrix multiplication.

## Notes
The workload sources wrap the ROI (matmul) with m5_reset_stats and m5_dump_stats; be sure to include and link m5ops accordingly. Also important to note that this will also create two stat blocks in stats.txt; always consider the first.