import os
import json
import argparse
import matplotlib.pyplot as plt
import seaborn as sns

from configs import (
    assocs,
    block_sizes,
    cache_sizes,
    init_block_sizes,
    matrix_sizes,
)

# Static configuration
metric_json_dir = "metric_jsons"
cache_size_order = {cs: i for i, cs in enumerate(cache_sizes)}
matrix_sizes = [100, 128, 200, 256, 512]

def load_metric_data(metric):
    with open(os.path.join(metric_json_dir, f"{metric}.json")) as f:
        return json.load(f)

def plot_metric(metric, run_type, output_dir):
    data = load_metric_data(metric)
    fig, axes = plt.subplots(len(matrix_sizes), len(assocs),
                             figsize=(14, 18), sharex=True, sharey=False)
    fig.suptitle(f"Metric: {metric} ({run_type})", fontsize=20)

    for row_idx, msize in enumerate(matrix_sizes):
        for col_idx, assoc in enumerate(assocs):
            ax = axes[row_idx, col_idx]
            curves = {}  # {block_size: [(cache, value)]}

            for entry in data:
                if entry["matrix"] != msize or entry["assoc"] != assoc:
                    continue
                if entry["type"] != run_type:
                    continue
                curves.setdefault(entry["block"], []).append((entry["cache"], entry["value"]))

            for block_size, points in sorted(curves.items()):
                label = "base" if block_size == 0 else f"b{block_size}"
                xs, ys = zip(*sorted(points, key=lambda x: cache_size_order[x[0]]))
                ax.plot(xs, ys, label=label)

            ax.set_title(f"Matrix {msize}, Assoc {assoc}")
            ax.set_xlabel("Cache Size")
            ax.set_ylabel(metric)
            ax.grid(True)

            
            ax.legend(fontsize="small", ncol=2)

    plt.tight_layout(rect=[0, 0, 1, 0.97])
    plt.savefig(os.path.join(output_dir, f"{metric}.png"))
    plt.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", choices=["ns", "ps"], required=True, help="Choose run type to plot: ns or ps")
    args = parser.parse_args()

    output_dir = f"big_plots{'-ps' if args.type == 'ps' else '-ns'}"
    os.makedirs(output_dir, exist_ok=True)

    for fname in os.listdir(metric_json_dir):
        if fname.endswith(".json"):
            metric = fname[:-5]
            plot_metric(metric, args.type, output_dir)

    print(f"Plots saved in {output_dir}")

if __name__ == "__main__":
    main()
