matrix_sizes = [100, 128, 200, 256, 512, 1024]
block_sizes = {}
cache_sizes = ["16kB", "32kB", "64kB"]
assocs = [4, 8]
stat_labels = [
    "simTicks",
    "simInsts",
    "system.cpu.cpi",
    "system.cpu.dcache.demandHits::total",
    "system.cpu.dcache.demandMisses::total",
    "system.cpu.dcache.demandAccesses::total",
    "system.cpu.icache.demandHits::total",
    "system.cpu.icache.demandMisses::total",
    "system.cpu.icache.demandAccesses::total",
]
axis_params = [cache_sizes, assocs]


def init_block_sizes():
    """
    Initialize block sizes for each matrix size.
    """
    for msize in matrix_sizes:
        bsize = 16
        bsizes = [0]
        while bsize <= msize:
            bsizes.append(bsize)
            bsize *= 2
        block_sizes[msize] = bsizes
