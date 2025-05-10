#!/bin/bash

start_time=$(date +%s)

# Define matrix sizes
matrix_sizes=(100 128 200 256) # leave out 512 for now

# Path to gem5 binary and Python script
GEM5_PATH="../build/X86/gem5.opt"
SCRIPT_PATH="system_l1.py"

# Clean up old output directories and stat files
echo ">>> Cleaning up old output directories and stat files..."
rm -rf l1_base_* l1_block_* catstat_*

# Run matmul-base with each matrix size
for size in "${matrix_sizes[@]}"; do
    outdir="l1_base_${size}"
    echo ""
    echo ">>> Running matmul-base with size ${size} -> ${outdir} ..."
    ${GEM5_PATH} --outdir=${outdir} ${SCRIPT_PATH} -- matmul-base ${size}
done

# Run matmul-blocked with each matrix size and suitable block sizes
for size in "${matrix_sizes[@]}"; do
    block=16
    while [ $block -le $size ]; do
        outdir="l1_block_${size}_${block}"
        echo ""
        echo ">>> Running matmul-blocked with matrix size ${size} and block size ${block} -> ${outdir} ..."
        ${GEM5_PATH} --outdir=${outdir} ${SCRIPT_PATH} -- matmul-blocked ${size} ${block}
        if [ $block -eq $size ]; then
            break
        fi
        block=$((block * 2))
        if [ $block -gt $size ]; then
            block=$size
        fi
    done
done

# Gather stats into grouped files
echo ""
echo ">>> Gathering stats into grouped files..."
for size in "${matrix_sizes[@]}"; do
    output_file="catstat_${size}"
    echo "Creating ${output_file}"
    : > "$output_file"

    # Add base stats first
    base_dir="l1_base_${size}"
    stats_file="${base_dir}/stats.txt"
    if [ -f "$stats_file" ]; then
        echo "[$base_dir]" >> "$output_file"
        sed -n '3,18p;118,137p;253,272p' "$stats_file" >> "$output_file"
        echo >> "$output_file"
    fi

    # Add blocked stats sorted by block size
    for dir in $(ls -d l1_block_${size}_* 2>/dev/null | sort -t_ -k4 -n); do
        stats_file="${dir}/stats.txt"
        if [ -f "$stats_file" ]; then
            echo "[$dir]" >> "$output_file"
            sed -n '3,18p;118,137p;253,272p' "$stats_file" >> "$output_file"
            echo >> "$output_file"
        fi
    done
done

end_time=$(date +%s)
elapsed=$((end_time - start_time))
echo "Total script runtime: ${elapsed} seconds"
