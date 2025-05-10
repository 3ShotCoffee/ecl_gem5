import os

import matplotlib.pyplot as plt

# Configurations
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

# One hue group per matrix size, different line styles per associativity
matrix_colors = {
    100: "red",  # red hues
    128: "gold",  # yellow hues
    200: "green",  # green hues
    256: "blue",  # blue hues
}

line_styles = {1: "-", 2: "--", 4: "-.", 8: ":"}


# Load stats from a file
def load_stats(stats_file_path):
    stats = {}
    if not os.path.exists(stats_file_path):
        return stats
    with open(stats_file_path) as f:
        for line in f:
            if "End" in line:
                # Stop reading if we reach the end of the first stats block
                break
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


# Generate plots
for csize in cache_sizes:
    for rp in replacement_policies:
        plot_dir = f"plots/{csize}_{rp}"
        os.makedirs(plot_dir, exist_ok=True)

        for stat_label in stat_labels:
            plt.figure(figsize=(12, 6))
            legend_labels = []

            for matrix_size in matrix_sizes:
                for assoc in assocs:
                    x_vals = []
                    y_vals = []
                    labels = []

                    # Base
                    base_dir = f"out/{matrix_size}_base/{csize}_{assoc}_{rp}"
                    stats = load_stats(os.path.join(base_dir, "stats.txt"))
                    if stats:
                        x_vals.append(0)
                        y_vals.append(stats.get(stat_label, 0))
                        labels.append("base")

                    # Blocked
                    bsize = 16
                    idx = 1
                    while bsize <= matrix_size:
                        blk_dir = (
                            f"out/{matrix_size}_{bsize}/{csize}_{assoc}_{rp}"
                        )
                        stats = load_stats(os.path.join(blk_dir, "stats.txt"))
                        if stats:
                            x_vals.append(idx)
                            y_vals.append(stats.get(stat_label, 0))
                            labels.append(str(bsize))
                        if bsize == matrix_size:
                            break
                        bsize *= 2
                        if bsize > matrix_size and bsize // 2 != matrix_size:
                            bsize = matrix_size
                        idx += 1

                    if x_vals:
                        label = f"{matrix_size}-assoc{assoc}"
                        legend_labels.append(label)
                        # print(legend_labels)
                        plt.plot(
                            x_vals,
                            y_vals,
                            label=label,
                            color=matrix_colors[matrix_size],
                            linestyle=line_styles[assoc],
                            marker="",
                        )

            plt.xticks(ticks=range(len(labels)), labels=labels)
            plt.xlabel("Block Size (or base)")
            plt.ylabel(stat_label)
            plt.title(f"{stat_label} ({csize}, {rp})")
            plt.legend(legend_labels, fontsize="small", ncol=2)
            plt.grid(True)
            plt.tight_layout()
            out_path = os.path.join(
                plot_dir, f"{stat_label.replace('::', '_')}.png"
            )
            plt.savefig(out_path)
            plt.close()

print("All plots generated and organized under 'plots/' directory.")
