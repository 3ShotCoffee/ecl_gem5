# Re-import libraries due to kernel reset
import os

import matplotlib.pyplot as plt

# Configuration
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

# Plot styling
matrix_colors = {100: "red", 128: "orange", 200: "green", 256: "blue"}
block_styles = {
    "base": "-",
    16: "--",
    32: "-.",
    64: ":",
    128: (0, (1, 10)),
    256: (0, (5, 10)),
}


# Load stats
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


# Main plot generation
axis_params = {
    "assoc": assocs,
    "csize": cache_sizes,
    "rp": replacement_policies,
}

for axis_param, axis_values in axis_params.items():
    other_keys = [k for k in axis_params if k != axis_param]
    other1_vals = axis_params[other_keys[0]]
    other2_vals = axis_params[other_keys[1]]

    for other1 in other1_vals:
        for other2 in other2_vals:
            plot_dir = f"plots/{axis_param}/{other1}_{other2}"
            os.makedirs(plot_dir, exist_ok=True)

            for stat_label in stat_labels:
                plt.figure(figsize=(12, 6))

                for matrix_size in matrix_sizes:
                    # Base config
                    x_vals, y_vals = [], []
                    for x in axis_values:
                        assoc = (
                            x
                            if axis_param == "assoc"
                            else (
                                other1
                                if other_keys[0] == "assoc"
                                else (
                                    other2
                                    if other_keys[1] == "assoc"
                                    else None
                                )
                            )
                        )
                        csize = (
                            x
                            if axis_param == "csize"
                            else (
                                other1
                                if other_keys[0] == "csize"
                                else (
                                    other2
                                    if other_keys[1] == "csize"
                                    else None
                                )
                            )
                        )
                        rp = (
                            x
                            if axis_param == "rp"
                            else (
                                other1
                                if other_keys[0] == "rp"
                                else other2 if other_keys[1] == "rp" else None
                            )
                        )

                        stat_path = f"out/{matrix_size}_base/{csize}_{assoc}_{rp}/stats.txt"
                        stats = load_stats(stat_path)
                        if stats:
                            x_vals.append(x)
                            y_vals.append(stats.get(stat_label, 0))

                    if x_vals:
                        plt.plot(
                            x_vals,
                            y_vals,
                            label=f"{matrix_size}-base",
                            color=matrix_colors[matrix_size],
                            linestyle=block_styles["base"],
                        )

                    # Blocked configs
                    bsize = 16
                    while bsize <= matrix_size:
                        x_vals, y_vals = [], []
                        for x in axis_values:
                            assoc = (
                                x
                                if axis_param == "assoc"
                                else (
                                    other1
                                    if other_keys[0] == "assoc"
                                    else (
                                        other2
                                        if other_keys[1] == "assoc"
                                        else None
                                    )
                                )
                            )
                            csize = (
                                x
                                if axis_param == "csize"
                                else (
                                    other1
                                    if other_keys[0] == "csize"
                                    else (
                                        other2
                                        if other_keys[1] == "csize"
                                        else None
                                    )
                                )
                            )
                            rp = (
                                x
                                if axis_param == "rp"
                                else (
                                    other1
                                    if other_keys[0] == "rp"
                                    else (
                                        other2
                                        if other_keys[1] == "rp"
                                        else None
                                    )
                                )
                            )

                            stat_path = f"out/{matrix_size}_{bsize}/{csize}_{assoc}_{rp}/stats.txt"
                            stats = load_stats(stat_path)
                            if stats:
                                x_vals.append(x)
                                y_vals.append(stats.get(stat_label, 0))

                        if x_vals:
                            plt.plot(
                                x_vals,
                                y_vals,
                                label=f"{matrix_size}-{bsize}",
                                color=matrix_colors[matrix_size],
                                linestyle=block_styles.get(bsize, "-"),
                            )

                        bsize *= 2

                plt.xlabel(axis_param)
                plt.ylabel(stat_label)
                plt.title(f"{stat_label} ({other1}_{other2})")
                plt.grid(True)
                plt.legend(fontsize="small", ncol=2)
                plt.tight_layout()
                out_file = os.path.join(
                    plot_dir, f"{stat_label.replace('::', '_')}.png"
                )
                plt.savefig(out_file)
                plt.close()

print("Completed generating switched-role plots.")
