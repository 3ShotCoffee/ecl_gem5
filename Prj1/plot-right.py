import os
import matplotlib.pyplot as plt
from configs import *

line_styles = {
    0: '-',
    1: '--',
    2: '-.',
    3: ':'
}
colors = ['red', 'green', 'blue', 'orange', 'purple', 'cyan', 'brown', 'pink']

# Utility to load stats from a file
def load_stats(path):
    stats = {}
    if not os.path.exists(path):
        return stats
    with open(path, 'r') as f:
        for line in f:
            if "End" in line:
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

all_params = {
    'assoc': assocs,
    'csize': cache_sizes,
    'rp': replacement_policies
}

x_param_keys = ['assoc', 'csize', 'rp']

# Helper: Generate label and color/style assignment
for x_param in x_param_keys:
    os.makedirs(f"plots/{x_param}", exist_ok=True)
    x_values = all_params[x_param]
    other_params = [p for p in x_param_keys if p != x_param]
    longer_param, shorter_param = sorted(other_params, key=lambda p: len(all_params[p]), reverse=True)

    color_map = {v: colors[i % len(colors)] for i, v in enumerate(all_params[longer_param])}
    style_map = {v: line_styles[i % len(line_styles)] for i, v in enumerate(all_params[shorter_param])}

    for msize in matrix_sizes:
        bsize = 16
        block_sizes = []
        while bsize < msize:
            block_sizes.append(bsize)
            bsize *= 2
        block_sizes.append(msize)  # include full matrix size as block size

        for block in [None] + block_sizes:
            block_label = "base" if block is None else str(block)
            subdir = f"plots/{x_param}/{msize}_{block_label}"
            os.makedirs(subdir, exist_ok=True)

            for stat_label in stat_labels:
                plt.figure(figsize=(10, 6))

                for long_val in all_params[longer_param]:
                    for short_val in all_params[shorter_param]:
                        y_vals = []
                        for x_val in x_values:
                            param_combo = {
                                x_param: x_val,
                                longer_param: long_val,
                                shorter_param: short_val
                            }

                            csize = param_combo['csize']
                            assoc = param_combo['assoc']
                            rp = param_combo['rp']

                            if block is None:
                                out_dir = f"out/{msize}_base/{csize}_{assoc}_{rp}"
                            else:
                                out_dir = f"out/{msize}_{block}/{csize}_{assoc}_{rp}"

                            stats = load_stats(os.path.join(out_dir, "stats.txt"))
                            val = stats.get(stat_label, 0)
                            y_vals.append(val)

                        label = f"{long_val}, {short_val}"
                        plt.plot(x_values, y_vals,
                                 label=label,
                                 color=color_map[long_val],
                                 linestyle=style_map[short_val],
                                 marker='o')

                plt.xlabel(x_param)
                plt.ylabel(stat_label)
                plt.title(f"{stat_label} ({msize}_{block_label})")
                plt.legend(fontsize='small', ncol=2)
                plt.grid(True)
                plt.tight_layout()

                out_file = f"{stat_label.replace('::', '_')}.png"
                plt.savefig(os.path.join(subdir, out_file))
                plt.close()

print("Sweep plots generated.")
