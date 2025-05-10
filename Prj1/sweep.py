import itertools
import subprocess
import os
import shutil
import time

# Experiment parameters
matrix_sizes = [100, 128, 200, 256]
cache_sizes = ['16kB', '32kB', '64kB']
assocs = [1, 2, 4, 8]
replacement_policies = ['FIFO', 'SecondChance', 'LFU', 'LRU', 'MRU', 'Random']
prefetchers = ['NULL', 'stride', 'tagged']
write_allocators = [True, False]

gem5_exe = "../build/X86/gem5.opt"
script = "system_l1.py"

# Output directory
out_root = "out"

# Start timing
start_time = time.time()

# Remove previous results if `out/` exists
if os.path.exists(out_root):
    print(f"Removing existing directory '{out_root}'...")
    shutil.rmtree(out_root)
os.makedirs(out_root)

def run_simulation(outdir, args):
    full_outdir = os.path.join(out_root, outdir)
    os.makedirs(full_outdir, exist_ok=True)  # Create the directory structure
    cmd = [gem5_exe, f"--outdir={full_outdir}", script] + args

    print("Running:", " ".join(cmd))
    subprocess.run(cmd)

for size, assoc, rp, pf, wa in itertools.product(cache_sizes, assocs, replacement_policies, prefetchers, write_allocators):
    # size_str = size.replace("kB", "")
    wa_str = str(wa).lower()
    config_str = f"{size}_{assoc}_{rp}_{pf}_{wa_str}"

    for msize in matrix_sizes:
        # matmul-base
        outdir = f"{msize}_base/{config_str}"
        args = [
            f"--l1d_size={size}",
            f"--l1d_assoc={assoc}",
            f"--l1d_rp={rp}",
            f"--l1d_pf={pf}",
            f"--l1d_wa={wa_str}",
            "matmul-base", str(msize)
        ]
        run_simulation(outdir, args)

        # matmul-blocked
        bsize = 16
        while bsize <= msize:
            outdir = f"{msize}_{bsize}/{config_str}"
            args = [
                f"--l1d_size={size}",
                f"--l1d_assoc={assoc}",
                f"--l1d_rp={rp}",
                f"--l1d_pf={pf}",
                f"--l1d_wa={wa_str}",
                "matmul-blocked", str(msize), str(bsize)
            ]
            run_simulation(outdir, args)

            if bsize == msize:
                break
            bsize *= 2
            if bsize > msize and bsize // 2 != msize:
                bsize = msize  # Ensure matrix size is included if not a power of 2

# End timing and print total runtime
end_time = time.time()
total_time_sec = end_time - start_time
print(f"\nTotal script runtime: {total_time_sec:.2f} seconds ({total_time_sec/60:.2f} minutes)")