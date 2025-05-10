from PIL import Image, ImageDraw, ImageFont
import os

image_files = [
    "plot_simInsts.png",
    "plot_simOps.png",
    "plot_simSeconds.png",
    "plot_simTicks.png",
    "plot_system.cpu.cpi.png",
    "plot_system.cpu.ipc.png",
    "plot_system.cpu.dcache.demandHits_total.png",
    "plot_system.cpu.dcache.demandMisses_total.png",
    "plot_system.cpu.dcache.demandAccesses_total.png",
    "plot_system.cpu.icache.demandHits_total.png",
    "plot_system.cpu.icache.demandMisses_total.png",
    "plot_system.cpu.icache.demandAccesses_total.png",
]

plot_root = "plots"

# Try to load a default font
try:
    font = ImageFont.truetype("arial.ttf", 24)
except:
    font = ImageFont.load_default()

# Open all images
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
final_img = Image.new('RGB', (final_width, final_height), color='white')
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
final_img.save("combined_plots_with_labels.png")
