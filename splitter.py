import os
from PIL import Image

# Configurable paths
INPUT_DIR = "data"
OUTPUT_DIR = "split_data"

# Supported image formats
VALID_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".webp")


def split_images_lossless(input_folder, output_folder, rows=5, cols=3):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if not filename.lower().endswith(VALID_EXTENSIONS):
            continue

        img_path = os.path.join(input_folder, filename)
        name, ext = os.path.splitext(filename)

        with Image.open(img_path) as img:
            # 1. Maintain original color mode (prevents color distortion)
            img = img.convert("RGB") if img.mode == "P" else img

            width, height = img.size

            # Precise float-based boundaries to prevent uneven slicing
            row_height = height / rows
            col_width = width / cols

            for r in range(rows):
                for c in range(cols):
                    # Round precise boundaries to integer pixels
                    left = int(round(c * col_width))
                    upper = int(round(r * row_height))
                    right = int(round((c + 1) * col_width))
                    lower = int(round((r + 1) * row_height))

                    cropped = img.crop((left, upper, right, lower))

                    # 2. Prevent Compression Loss: Save at 100% quality or as PNG
                    output_filename = f"{name}_r{r+1}_c{c+1}.png"  # Forcing PNG avoids JPEG artifacts
                    save_path = os.path.join(output_folder, output_filename)

                    cropped.save(save_path, format="PNG", optimize=True)


if __name__ == "__main__":
    split_images_lossless(INPUT_DIR, OUTPUT_DIR, rows=5, cols=3)