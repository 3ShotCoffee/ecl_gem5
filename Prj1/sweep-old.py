import itertools
import subprocess
import os
import shutil
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

# Sweep parameters
matrix_sizes = [100, 128, 200, 256]
cache_sizes = ['16kB', '32kB', '64kB']
assocs = [1, 2, 4, 8]
replacement_policies = ['FIFO', 'SecondChance', 'LFU', 'LRU', 'MRU', 'Random']
prefetchers = ['NULL', 'stride', 'tagged']
write_allocators = [True, False]

gem5_exe = "../build/X86/gem5.opt"
script = "system_l1.py"
out_root = "out"
max_workers = 32  # Adjust to use fewer cores if needed

def construct_job(msize, bsize, is_blocked, size, assoc, rp, pf, wa):
    size_str = size.replace("kB", "")
    wa_str = str(wa).lower()
    config_str = f"{size_str}_{assoc}_{rp}_{pf}_{wa_str}"

    if is_blocked:
        outdir = os.path.join(out_root, f"{msize}_{bsize}", config_str)
        args = [
            f"--l1d_size={size}",
            f"--l1d_assoc={assoc}",
            f"--l1d_rp={rp}",
            f"--l1d_pf={pf}",
            f"--l1d_wa={wa_str}",
            "matmul-blocked", str(msize), str(bsize)
        ]
    else:
        outdir = os.path.join(out_root, f"{msize}_base", config_str)
        args = [
            f"--l1d_size={size}",
            f"--l1d_assoc={assoc}",
            f"--l1d_rp={rp}",
            f"--l1d_pf={pf}",
            f"--l1d_wa={wa_str}",
            "matmul-base", str(msize)
        ]

    return (outdir, args)

def run_simulation(job):
    outdir, args = job
    os.makedirs(outdir, exist_ok=True)
    cmd = [gem5_exe, f"--outdir={outdir}", script] + args
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return outdir

def main():
    start_time = time.time()

    # Clean output directory
    if os.path.exists(out_root):
        print(f"Removing existing output directory '{out_root}'...")
        shutil.rmtree(out_root)
    os.makedirs(out_root)

    # Build the job list
    jobs = []
    for size, assoc, rp, pf, wa in itertools.product(cache_sizes, assocs, replacement_policies, prefetchers, write_allocators):
        for msize in matrix_sizes:
            # matmul-base
            jobs.append(construct_job(msize, None, False, size, assoc, rp, pf, wa))

            # matmul-blocked
            bsize = 16
            while bsize <= msize:
                jobs.append(construct_job(msize, bsize, True, size, assoc, rp, pf, wa))
                if bsize == msize:
                    break
                bsize *= 2
                if bsize > msize and bsize // 2 != msize:
                    bsize = msize

    print(f"Total jobs to run: {len(jobs)}")

    # Run in parallel using ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(run_simulation, job): job for job in jobs}
        for i, future in enumerate(as_completed(futures), 1):
            outdir = futures[future][0]
            try:
                future.result()
                print(f"[{i}/{len(jobs)}] Finished: {outdir}")
            except Exception as e:
                print(f"Error running job {outdir}: {e}")

    total_time = time.time() - start_time
    print(f"\nTotal runtime: {total_time:.2f} seconds ({total_time/60:.2f} minutes)")

if __name__ == "__main__":
    main()
