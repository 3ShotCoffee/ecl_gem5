import os

from PIL import (
    Image,
    ImageDraw,
    ImageFont,
)

cache_sizes = ["16kB", "32kB", "64kB"]
replacement_policies = ["FIFO", "LFU", "LRU", "MRU", "Random"]

image_files = [
    "simTicks.png",
    "simInsts.png",
    "system.cpu.cpi.png",
    "system.cpu.dcache.demandHits_total.png",
    "system.cpu.dcache.demandMisses_total.png",
    "system.cpu.dcache.demandAccesses_total.png",
    "system.cpu.icache.demandHits_total.png",
    "system.cpu.icache.demandMisses_total.png",
    "system.cpu.icache.demandAccesses_total.png",
]

# Try to load a default font
try:
    font = ImageFont.truetype("arial.ttf", 24)
except:
    font = ImageFont.load_default()

# Generate the first type of plots: one image per cache size and replacement policy
for csize in cache_sizes:
    for rp in replacement_policies:

        # Open all images
        plot_root = f"plots/{csize}_{rp}"
        images = [Image.open(os.path.join(plot_root, f)) for f in image_files]

        # Layout parameters
        cols = 3  # Number of images per row
        rows = (len(images) + cols - 1) // cols
        img_width, img_height = images[0].size
        label_height = 40  # Space above each image for a label

        # Final canvas size
        final_width = cols * img_width
        final_height = rows * (img_height + label_height)

        # Create a new blank white image
        final_img = Image.new(
            "RGB", (final_width, final_height), color="white"
        )
        draw = ImageDraw.Draw(final_img)

        # Paste each image and add label
        for idx, (img, fname) in enumerate(zip(images, image_files)):
            x = (idx % cols) * img_width
            y = (idx // cols) * (img_height + label_height)

            # Draw the label centered
            label = fname.replace(".png", "")
            text_width = draw.textlength(label, font=font)
            text_x = x + (img_width - text_width) // 2
            draw.text((text_x, y + 10), label, fill="black", font=font)

            # Paste the image below the label
            final_img.paste(img, (x, y + label_height))

        # Save final output
        final_img.save(f"plots/comb/{csize}_{rp}.png")

# Generate the second type of plots: one image per statistic
for stat_label in image_files:
    # Open all images
    images = []
    for csize in cache_sizes:
        for rp in replacement_policies:
            plot_root = f"plots/{csize}_{rp}"
            img_path = os.path.join(plot_root, stat_label)
            if os.path.exists(img_path):
                images.append((Image.open(img_path), f"{csize}_{rp}"))

    # Layout parameters
    cols = len(replacement_policies)  # Number of images per row
    rows = (len(images) + cols - 1) // cols
    img_width, img_height = images[0][0].size
    label_height = 40  # Space above each image for a label

    # Final canvas size
    final_width = cols * img_width
    final_height = rows * (img_height + label_height)

    # Create a new blank white image
    final_img = Image.new("RGB", (final_width, final_height), color="white")
    draw = ImageDraw.Draw(final_img)

    # Paste each image and add label
    for idx, (img, label) in enumerate(images):
        x = (idx % cols) * img_width
        y = (idx // cols) * (img_height + label_height)

        # Draw the label centered
        text_width = draw.textlength(label, font=font)
        text_x = x + (img_width - text_width) // 2
        draw.text((text_x, y + 10), label, fill="black", font=font)

        # Paste the image below the label
        final_img.paste(img, (x, y + label_height))

    # Save final output
    final_img.save(f"plots/comb/{stat_label}.png")

print("All combined plots generated and organized under 'plots/' directory.")
