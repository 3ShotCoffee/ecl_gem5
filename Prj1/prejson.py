import os
import re
import json
from pathlib import Path

from configs import (
    matrix_sizes,
    cache_sizes,
    assocs,
    stat_labels_rep,
    init_block_sizes,
    block_sizes,
)

# Until 1024 is done
matrix_sizes = [100, 128, 200, 256, 512]

init_block_sizes()

# Define search paths
base_dirs = {"ns": "out", "ps": "out-ps"}

# Initialize data structure for each metric
metric_data = {short: [] for short in stat_labels_rep.values()}

# Function to parse stats.txt and extract values
def parse_stats(stats_path, stat_labels_rep):
    values = {}
    if not stats_path.is_file():
        return None
    with open(stats_path) as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                stat = parts[0]
                if stat in stat_labels_rep:
                    values[stat_labels_rep[stat]] = float(parts[1])
    return values

# Traverse directories and collect data
for dtype, base_dir in base_dirs.items():
    for msize in matrix_sizes:
        for bsize in block_sizes[msize]:
            sim_dir = Path(base_dir) / f"{msize}_{bsize}"
            for csize in cache_sizes:
                for assoc in assocs:
                    stat_path = sim_dir / f"{csize}_{assoc}" / "stats.txt"
                    stats = parse_stats(stat_path, stat_labels_rep)
                    if stats:
                        for key, val in stats.items():
                            metric_data[key].append({
                                "matrix": msize,
                                "block": bsize,
                                "cache": csize,
                                "assoc": assoc,
                                "type": dtype,
                                "value": val
                            })

# Write each metric to its own JSON file
output_dir = Path("metric_jsons")
output_dir.mkdir(parents=True, exist_ok=True)

json_paths = []
for metric, entries in metric_data.items():
    out_path = output_dir / f"{metric}.json"
    with open(out_path, "w") as f:
        json.dump(entries, f, indent=2)
    json_paths.append(out_path)

json_paths
