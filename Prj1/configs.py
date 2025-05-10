matrix_sizes = [100, 128, 200, 256]
cache_sizes = ["16kB", "32kB", "64kB"]
assocs = [1, 2, 4, 8]
replacement_policies = ["FIFO", "LFU", "LRU", "MRU", "Random"]
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
axis_params = {
    "assoc": assocs,
    "csize": cache_sizes,
    "rp": replacement_policies,
}
