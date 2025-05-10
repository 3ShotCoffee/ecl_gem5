import os

import matplotlib.pyplot as plt

# Configurations
matrix_sizes = [100, 128, 200, 256]
stat_labels = [
    "simSeconds",
    "simTicks",
    "simInsts",
    "simOps",
    "system.cpu.cpi",
    "system.cpu.ipc",
    "system.cpu.dcache.demandHits::total",
    "system.cpu.dcache.demandMisses::total",
    "system.cpu.dcache.demandAccesses::total",
    "system.cpu.icache.demandHits::total",
    "system.cpu.icache.demandMisses::total",
    "system.cpu.icache.demandAccesses::total",
]

matrix_colors = ["blue", "green", "red", "orange"]  # One color per matrix size


# Load stats from a file
def load_stats(stats_file_path):
    stats = {}
    if not os.path.exists(stats_file_path):
        return stats
    with open(stats_file_path) as f:
        for line in f:
            if line.strip().startswith("#") or line.strip() == "":
                continue
            parts = line.strip().split()
            if len(parts) >= 2:
                key = parts[0]
                try:
                    value = float(parts[1])
                except ValueError:
                    continue
                stats[key] = value
    return stats


# Collect all data
data_by_matrix = {size: {} for size in matrix_sizes}
block_sizes_map = {}

for matrix_size in matrix_sizes:
    # Base
    base_path = f"l1_base_{matrix_size}/stats.txt"
    stats = load_stats(base_path)
    if stats:
        data_by_matrix[matrix_size]["base"] = stats

    # Blocked
    block = 16
    blocks_used = []
    while block <= matrix_size:
        path = f"l1_block_{matrix_size}_{block}/stats.txt"
        stats = load_stats(path)
        if stats:
            data_by_matrix[matrix_size][block] = stats
            blocks_used.append(block)
        if block == matrix_size:
            break
        block *= 2
        if block > matrix_size:
            block = matrix_size
    block_sizes_map[matrix_size] = blocks_used

# Plot: one figure per stat, each with multiple lines (matrix sizes)
for stat_index, stat_label in enumerate(stat_labels):
    plt.figure(figsize=(12, 6))

    for color_index, matrix_size in enumerate(matrix_sizes):
        keys = ["base"] + block_sizes_map[matrix_size]
        x_labels = [str(k) for k in keys]
        x = list(range(len(keys)))
        y = [
            data_by_matrix[matrix_size].get(k, {}).get(stat_label, 0)
            for k in keys
        ]

        plt.plot(
            x,
            y,
            marker="o",
            label=f"Matrix {matrix_size}",
            color=matrix_colors[color_index],
        )

    plt.xticks(range(len(x_labels)), x_labels)
    plt.xlabel("Block Size (or base)")
    plt.ylabel(stat_label)
    plt.title(f"{stat_label}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    filename = fr"plots\plot_{stat_label.replace('::', '_')}.png"
    plt.savefig(filename)
    plt.close()

print("All plots generated: one per statistic.")
