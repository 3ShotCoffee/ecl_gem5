from PIL import Image, ImageDraw, ImageFont
import os
from math import log2, floor

# Configuration
matrix_sizes = [100, 128, 200, 256]
cache_sizes = ['16kB', '32kB', '64kB']
assocs = [1, 2, 4, 8]
replacement_policies = ['FIFO', 'LFU', 'LRU', 'MRU', 'Random']
axis_params = ['assoc', 'csize', 'rp']
stat_label = "system.cpu.cpi.png"

# Try to load a default font
try:
    font = ImageFont.truetype("arial.ttf", 24)
except:
    font = ImageFont.load_default()

for axis_param in axis_params:
    images = []
    axis_root = f"plots/{axis_param}"

    # Build the other two parameter sets
    if axis_param == 'assoc':
        other_pairs = [(c, r) for c in cache_sizes for r in replacement_policies]
        subdir_names = [f"{c}_{r}" for c, r in other_pairs]
    elif axis_param == 'csize':
        other_pairs = [(a, r) for a in assocs for r in replacement_policies]
        subdir_names = [f"{a}_{r}" for a, r in other_pairs]
    elif axis_param == 'rp':
        other_pairs = [(a, c) for a in assocs for c in cache_sizes]
        subdir_names = [f"{a}_{c}" for a, c in other_pairs]
    else:
        continue  # invalid

    # For each subdir, attempt to open the image
    for idx, subdir in enumerate(subdir_names):
        img_path = os.path.join(axis_root, subdir, stat_label)
        if os.path.exists(img_path):
            images.append((Image.open(img_path), idx))

    if not images:
        continue

    # Layout parameters
    cols = 5  # number of images per row
    rows = (len(images) + cols - 1) // cols
    img_width, img_height = images[0][0].size
    final_width = cols * img_width
    final_height = rows * img_height

    # Create a blank white canvas
    final_img = Image.new('RGB', (final_width, final_height), color='white')
    draw = ImageDraw.Draw(final_img)

    # Paste images
    for img, idx in images:
        x = (idx % cols) * img_width
        y = (idx // cols) * img_height
        final_img.paste(img, (x, y))

    # Save final image
    final_img.save(f"plots/left_{axis_param}_cpi.png")

print("All combined plots generated and organized under 'plots/' directory.")
