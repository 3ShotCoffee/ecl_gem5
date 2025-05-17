import os
import matplotlib.pyplot as plt

from configs import (
    assocs,
    block_sizes,
    cache_sizes,
    init_block_sizes,
    matrix_sizes,
    stat_labels,
)

colors = ["red", "green", "blue", "orange", "purple", "cyan", "brown", "pink"]

def load_stats(path):
    stats = {}
    if not os.path.exists(path):
        return stats
    with open(path) as f:
        for line in f:
            if (
                "End" in line
                or line.strip().startswith("#")
                or not line.strip()
            ):
                continue
            parts = line.strip().split()
            if len(parts) >= 2:
                key = parts[0]
                try:
                    stats[key] = float(parts[1])
                except ValueError:
                    continue
    return stats


init_block_sizes()

for msize in matrix_sizes:
    for assoc in assocs:
        os.makedirs("plots/", exist_ok=True)

        for stat_label in stat_labels:
            plt.figure(figsize=(12, 6))

            for idx, bsize in enumerate(block_sizes[msize]):
                x_vals = []
                y_vals = []

                for csize in cache_sizes:
                    if bsize == 0:
                        out_dir = f"out/{msize}_base/{csize}_{assoc}"
                    else:
                        out_dir = f"out/{msize}_{bsize}/{csize}_{assoc}"

                    stats = load_stats(os.path.join(out_dir, "stats.txt"))
                    if not stats:
                        print(f"Warning: No stats found for {out_dir}")
                        continue
                    if stat_label not in stats:
                        print(f"Warning: {stat_label} not found in {out_dir}")
                        continue

                    x_vals.append(csize)
                    y_vals.append(stats[stat_label])

                if x_vals and y_vals:  # Only plot if there's data
                    plt.plot(
                        x_vals,
                        y_vals,
                        label="base" if bsize == 0 else f"block size = {bsize}",
                        color=colors[idx % len(colors)],
                        marker="o",
                    )

            plt.xlabel("Cache Size")
            plt.ylabel(stat_label)
            plt.title(f"{stat_label} (matrix size = {msize}, assoc = {assoc})")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()

            filename = f"plots/{msize}_{assoc}_{stat_label.replace('::', '_')}.png"
            plt.savefig(filename)
            plt.close()

print("All plots generated: one per statistic.")
