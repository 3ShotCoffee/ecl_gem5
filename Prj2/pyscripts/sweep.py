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
    seq_lens,
    block_sizes,
    init_block_sizes,
    axis_params,
    test_configs,
)

# matrix_sizes = [1024]
# axis_params = [["64kB"], [4, 8]]  # Cache sizes and associativity
init_block_sizes()

gem5_exe = "../../build/X86/gem5.opt"
script = "system_l1.py"
out_root = "../out"
workload = "../workload/attention"
max_workers = 22  # Adjust to use fewer cores if needed
SUCCESS_STRING = "Checksum"


def construct_job(csize, assoc, bsize, config):
    if bsize == 0:
        # Construct job for matrix multiplication with no tiling
        outdir = os.path.join(out_root, f"{config[0]}-{config[1]}-{config[2]}_base/{csize}_{assoc}")
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
        outdir = os.path.join(out_root, f"{config[0]}-{config[1]}-{config[2]}_{bsize}/{csize}_{assoc}")
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
    cmd = [gem5_exe, f"--outdir={outdir}", script] + args

    result = subprocess.run(cmd, capture_output=True, text=True)
    stdout = result.stdout.strip().splitlines()

    if result.returncode != 0:
        raise RuntimeError(f"Simulation failed (non-zero exit): {outdir}")

    if len(stdout) < 2 or SUCCESS_STRING not in stdout[-2]:
        raise RuntimeError(f"Incorrect output in: {outdir}")

    return outdir


def main():
    start_time = time.time()

    # Build the job list
    jobs = []
    for config in test_configs:
        for bsize in block_sizes[config[0]]:
            for csize, assoc in itertools.product(*axis_params):
                jobs.append(construct_job(csize, assoc, bsize, config))

    print(f"Total jobs to run: {len(jobs)}")

    completed = 0
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
                    print("Aborting remaining simulations...")
                    executor.shutdown(wait=False, cancel_futures=True)
                    raise SystemExit(1)

    except CancelledError:
        print("Execution was cancelled.")

    total_time = time.time() - start_time
    print(
        f"\nTotal runtime: {total_time:.2f} seconds ({total_time/60:.2f} minutes)"
    )


if __name__ == "__main__":
    main()
