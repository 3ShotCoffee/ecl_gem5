import itertools
import os
import shutil
import subprocess
import time
from concurrent.futures import (
    CancelledError,
    ProcessPoolExecutor,
    as_completed,
)

from configs import (
    axis_params,
    block_sizes,
    init_block_sizes,
    test_configs,
)

test_configs = [  # A list of (seq_len, hidden_dim, heads) tuples
    [64, 128, 8],  # Lightweight test
    [128, 256, 8],  # Still lightweight, but more expressive
    [128, 768, 12],  # Mirrors DistilBERT
]

init_block_sizes()

gem5_exe = "../../build/X86/gem5.opt"
script = "system_l1.py"
out_root = "../out"
workload = "../workload/attention"
max_workers = 22  # Adjust to use fewer cores if needed
SUCCESS_STRING = "Checksum"
END_STRING = "End Simulation Statistics"


def construct_job(csize, assoc, bsize, config):
    if bsize == 0:
        # Construct job for matrix multiplication with no tiling
        outdir = os.path.join(
            out_root,
            f"{config[0]}-{config[1]}-{config[2]}_base/{csize}_{assoc}",
        )
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        args = [
            f"--l1d_size={csize}",
            f"--l1d_assoc={assoc}",
            workload,
            str(config[0]),  # sequence length
            str(config[1]),  # hidden dimension
            str(config[2]),  # number of heads
            "base",
        ]
    else:
        # Construct job for blocked matrix multiplication (over ijk)
        outdir = os.path.join(
            out_root,
            f"{config[0]}-{config[1]}-{config[2]}_{bsize}/{csize}_{assoc}",
        )
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        args = [
            f"--l1d_size={csize}",
            f"--l1d_assoc={assoc}",
            workload,
            str(config[0]),  # sequence length
            str(config[1]),  # hidden dimension
            str(config[2]),  # number of heads
            "blocked",
            str(bsize),
        ]

    return (outdir, args)


def run_simulation(job):
    outdir, args = job
    os.makedirs(outdir, exist_ok=True)
    log_path = os.path.join(outdir, "log.txt")
    cmd = [gem5_exe, f"--outdir={outdir}", script] + args
    with open(log_path, "w") as log_file:
        result = subprocess.run(
            cmd, stdout=log_file, stderr=subprocess.STDOUT, text=True
        )

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Simulation failed (non-zero exit): {outdir}")

    return outdir


def main():
    start_time = time.time()

    # Build the job list
    jobs = []
    for config in test_configs:
        for bsize in block_sizes[config[0]]:
            for csize, assoc in itertools.product(*axis_params):
                job = construct_job(csize, assoc, bsize, config)
                outdir = job[0]
                stats_path = os.path.join(outdir, "stats.txt")
                should_run = True
                if os.path.isfile(stats_path):
                    with open(stats_path) as f:
                        count = sum(1 for line in f if END_STRING in line)
                    if count >= 2:
                        should_run = False

                if should_run:
                    jobs.append(job)
                else:
                    print(
                        f"✅ Skipping (stats.txt has ≥2 END_STRING): {outdir}"
                    )

    print(f"Total jobs to run: {len(jobs)}")

    completed = 0
    failed_jobs = []
    try:
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(run_simulation, job): job for job in jobs
            }
            for future in as_completed(futures):
                job = futures[future]
                outdir = job[0]
                try:
                    future.result()
                    completed += 1
                    print(
                        f"[{completed}/{len(jobs)}] Finished: {outdir}, time passed: {time.time() - start_time:.2f} seconds"
                    )
                except Exception as e:
                    print(f"\n❌ Error: {e}")
                    failed_jobs.append(job[0])

    except CancelledError:
        print("Execution was cancelled.")

    total_time = time.time() - start_time
    print(
        f"\nTotal runtime: {total_time:.2f} seconds ({total_time/60:.2f} minutes)"
    )

    print(f"\nCompleted {completed} jobs, failed {len(failed_jobs)} jobs.")


if __name__ == "__main__":
    main()
