matrix_sizes = [100, 128, 200, 256, 512, 1024]
block_sizes = {}
cache_sizes = ["16kB", "32kB", "64kB"]
assocs = [4, 8]
stat_labels_rep = {
    "simTicks" : "simTicks",
    "simInsts" : "simInsts",
    "system.cpu.cpi" : "cpi",
    "system.cpu.dcache.demandHits::total" : "d_Hits",
    "system.cpu.dcache.demandMisses::total" : "d_Misses",
    "system.cpu.dcache.demandAccesses::total" : "d_Accesses",
    "system.cpu.dcache.demandMissRate::total" : "d_MissRate", 
    "system.cpu.icache.demandHits::total" : "i_Hits",
    "system.cpu.icache.demandMisses::total" : "i_Misses",
    "system.cpu.icache.demandAccesses::total" : "i_Accesses",
    "system.cpu.icache.demandMissRate::total" : "i_MissRate",
}
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
