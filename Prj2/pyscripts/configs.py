block_sizes = {}
cache_sizes = ["16kB", "32kB", "64kB"]
assocs = [4, 8]
axis_params = [cache_sizes, assocs]
stat_labels = [
    "simTicks",
    "simInsts",
    "system.cpu.cpi",
    "system.cpu.dcache.demandHits::total",
    "system.cpu.dcache.demandMisses::total",
    "system.cpu.dcache.demandAccesses::total",
    "system.cpu.dcache.demandMissRate::total",
    "system.cpu.icache.demandHits::total",
    "system.cpu.icache.demandMisses::total",
    "system.cpu.icache.demandAccesses::total",
    "system.cpu.icache.demandMissRate::total",
]
stat_labels_rep = {
    "simTicks": "simTicks",
    "simInsts": "simInsts",
    "system.cpu.cpi": "cpi",
    "system.cpu.dcache.demandHits::total": "d_Hits",
    "system.cpu.dcache.demandMisses::total": "d_Misses",
    "system.cpu.dcache.demandAccesses::total": "d_Accesses",
    "system.cpu.dcache.demandMissRate::total": "d_MissRate",
    "system.cpu.icache.demandHits::total": "i_Hits",
    "system.cpu.icache.demandMisses::total": "i_Misses",
    "system.cpu.icache.demandAccesses::total": "i_Accesses",
    "system.cpu.icache.demandMissRate::total": "i_MissRate",
}
test_configs = [  # A list of (seq_len, hidden_dim, heads) tuples
    [64, 128, 8],  # Lightweight test
    [128, 256, 8],  # Still lightweight, but more expressive
    [128, 768, 12],  # Mirrors DistilBERT
    [256, 512, 8],  # Higher sequence, lower hidden
    [512, 1024, 16],  # Mirrors BERT-Large
]


def init_block_sizes():
    """
    Initialize block sizes for each sequence length (shorter side of the matrix).
    """
    for config in test_configs:
        seq_len = config[0]
        bsize = 16
        bsizes = [0]
        while bsize <= seq_len:
            bsizes.append(bsize)
            bsize *= 2
        block_sizes[seq_len] = bsizes


init_block_sizes()
print("Block sizes initialized:", block_sizes)
