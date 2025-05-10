import os
from math import (
    floor,
    log2,
)

from PIL import (
    Image,
    ImageDraw,
    ImageFont,
)

from configs import *

# Try to load a default font
try:
    font = ImageFont.truetype("arial.ttf", 24)
except:
    font = ImageFont.load_default()

images = []
for axis_param in axis_params:
    plot_root = f"plots/{axis_param}"
    for msize in matrix_sizes:
        img_path = os.path.join(
            plot_root, f"{msize}_base", "system.cpu.cpi.png"
        )
        if os.path.exists(img_path):
            idx = (0, matrix_sizes.index(msize))
            images.append((Image.open(img_path), idx))
        bsize = 16
        idx_x = 1
        while bsize <= msize:
            folder_suffix = f"{msize}_{bsize}"
            img_path = os.path.join(
                plot_root, folder_suffix, "system.cpu.cpi.png"
            )
            if os.path.exists(img_path):
                idx = (idx_x, matrix_sizes.index(msize))
                images.append((Image.open(img_path), idx))
            bsize *= 2
            idx_x += 1

    # Layout parameters
    rows = len(matrix_sizes)  # Number of rows
    cols = floor(log2(matrix_sizes[-1])) - 2  # Number of columns
    img_width, img_height = images[0][0].size

    # Final canvas size
    final_width = cols * img_width
    final_height = rows * img_height

    # Create a new blank white image
    final_img = Image.new("RGB", (final_width, final_height), color="white")
    draw = ImageDraw.Draw(final_img)

    # Paste each image and add label
    for _, (img, (idx_x, idx_y)) in enumerate(images):
        x = idx_x * img_width
        y = idx_y * img_height

        # Paste the image below the label
        final_img.paste(img, (x, y))

    # Save final output
    final_img.save(f"plots/right_{axis_param}_cpi.png")

print("All combined plots generated and organized under 'plots/' directory.")
