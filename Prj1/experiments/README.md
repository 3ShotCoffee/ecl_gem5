# experiments/
A directory for experiment scripts and outputs.

The subdirectories may or may not include scripts if they are redundant.
However, each subdirectories should include outputs:
* out : gem5 m5out directory (gitignored).
* metric_jsons : preprocessed json files grouped by stat types.
* big_plots : visualization of the json files.

## Overview
* block_jk : blocked matrix multiplication with blocking over j & k loops.
* block_ijk : blocked matrix multiplication with blocking over i, j & k loops.
* ijk_1024_8 : blocked_ijk with added case of 1024x1024 matmul with blocksize=8.
* incr_channels : sweep number of DRAM channels to increase DRAM bandwidth.
    * WIP: did not improve because the CPU was nonparallel.
* oblivious : cache-oblivious matrix multiplication.

## Notes
