import numpy as np
import pyvista as pv

from PIL import Image

band1 = Image.open("split_data\\rx1_r2_c2.png").convert("L")  # Convert to grayscale
band2 = Image.open("split_data\\rx2_r2_c2.png").convert("L")
band3 = Image.open("split_data\\w1_r2_c2.png").convert("L")
band4 = Image.open("split_data\\w2_r2_c2.png").convert("L")

band1 = np.array(band1)
band2 = np.array(band2)
band3 = np.array(band3)
band4 = np.array(band4)

shape = band1.shape
print(shape)

# Example input: 4 grayscale image arrays
# Replace these with your actual arrays
# band1 = np.random.randint(0, 256, (200, 300), dtype=np.uint8)
# band2 = np.random.randint(0, 256, (200, 300), dtype=np.uint8)
# band3 = np.random.randint(0, 256, (200, 300), dtype=np.uint8)
# band4 = np.random.randint(0, 256, (200, 300), dtype=np.uint8)
 
bands = [band1, band2, band3, band4]
 
plotter = pv.Plotter(window_size=shape)
plotter.set_background("white")
 
z_spacing = 50  # distance between layers
 
for i, arr in enumerate(bands):
    # Ensure uint8 grayscale
    arr = arr.astype(np.uint8)
 
    h, w = arr.shape
 
    # Convert grayscale array to RGB texture
    rgb = np.stack([arr, arr, arr], axis=-1)
    texture = pv.numpy_to_texture(rgb)
 
    # Create plane for this band
    plane = pv.Plane(
        center=(w / 2, h / 2, i * z_spacing),
        direction=(0, 0, 1),
        i_size=w,
        j_size=h,
        i_resolution=1,
        j_resolution=1,
    )
 
    plotter.add_mesh(plane, texture=texture, show_edges=False)
 
    # Add band label
    plotter.add_point_labels(
        [(w + 40, h / 2, i * z_spacing)],
        [f"Band {i + 1}"],
        font_size=14,
        show_points=False,
        always_visible=True,
        text_color="black",
    )
 
plotter.camera_position = "iso"
plotter.show()