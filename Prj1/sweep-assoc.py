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
    cache_sizes,
    block_sizes,
    init_block_sizes,
    matrix_sizes,
)

# Override configs for testing
matrix_sizes = [512]
axis_params = [cache_sizes, [1, 2]]

init_block_sizes()

gem5_exe = "../build/X86/gem5.opt"
script = "system_l1.py"
out_root = "out"
max_workers = 24  # Adjust to use fewer cores if needed
SUCCESS_STRING = "The sum is"


def construct_job(msize, bsize, csize, assoc):

    if bsize != 0:
        # Blocked
        outdir = os.path.join(out_root, f"{msize}_{bsize}/{csize}_{assoc}")
        args = [
            f"--l1d_size={csize}",
            f"--l1d_assoc={assoc}",
            "matmul-blocked",
            str(msize),
            str(bsize),
        ]
    else:
        # Base
        outdir = os.path.join(out_root, f"{msize}_base/{csize}_{assoc}")
        args = [
            f"--l1d_size={csize}",
            f"--l1d_assoc={assoc}",
            "matmul-base",
            str(msize),
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

    # Clean output directory
    # if os.path.exists(out_root):
    #     print(f"Removing existing output directory '{out_root}'...")
    #     shutil.rmtree(out_root)
    # os.makedirs(out_root)

    # Build the job list
    jobs = []
    for size, assoc in itertools.product(*axis_params):
        for msize in matrix_sizes:
            for bsize in block_sizes[msize]:
                jobs.append(construct_job(msize, bsize, size, assoc))

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
