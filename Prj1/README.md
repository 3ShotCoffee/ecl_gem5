# Prj1: simple matmul configurations
A repository for running matrix multiplications on a simple system with an L1 cache.

## Running gem5 Simulations
Syntax is: 
```plaintext
gem5 {parameters to gem5} {gem5 python config script} {script parameters}.
```
e.g. you can run a simulation with a 64kB sized cache with tiled matrix multiplication where the matrix size is 1024 x 1024 and block size 256 with the following command:
```plaintext
../build/X86/gem5.opt system_l1.py --l1d_size=64kB matmul-blocked 1024 256
```

## Source Tree
Prj1 directory includes the following files/subdirectories:
* workload/ : source and Makefile for the binaries to run. 
    * The binaries themselves should be placed right under Prj1/.
* system_l1.py & cache_l1.py : respectively define the system and L1 cache for simulation.
* configs.py : describe the system or binary configurations that should be run. 
* pyscripts/ : python scripts for processing experiment outputs.
    * sweep(-skip).py : script for sweeping configs. The output is the out/ directory.
    * prejson.py : aggregates the outputs by stat labels in JSON form. The output is the metric_jsons/ directory.
    * big-plot.py : visualizes the JSON files. The output is the big_plots/ directory.
* experiments/ : encapsulates related scripts and outputs.

## Notes
Read readme's in directories workload and experiments likewise.