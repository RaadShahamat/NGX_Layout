import numpy as np
import plotly.graph_objects as go
from skimage import exposure, img_as_float
from skimage.transform import resize
 
from PIL import Image

band1 = Image.open("split_data\\rx1_r2_c2.png").convert("L")  # Convert to grayscale
band2 = Image.open("split_data\\rx2_r2_c2.png").convert("L")
band3 = Image.open("split_data\\w1_r2_c2.png").convert("L")
band4 = Image.open("split_data\\w2_r2_c2.png").convert("L")

band1 = np.array(band1)
band2 = np.array(band2)
band3 = np.array(band3)
band4 = np.array(band4)
def prepare_band(arr, target_shape=None):
    """
    Convert input array to float, optionally resize, and normalize to [0, 1].
    """
    arr = np.asarray(arr)
 
    if arr.ndim != 2:
        raise ValueError("Each band must be a 2D NumPy array.")
 
    arr = img_as_float(arr)
 
    if target_shape is not None and arr.shape != target_shape:
        arr = resize(arr, target_shape, preserve_range=True, anti_aliasing=True)
 
    arr = exposure.rescale_intensity(arr, in_range='image', out_range=(0, 1))
    return arr
 
 
def show4(band1, band2, band3, band4, z_spacing=20, opacity=0.95):
    bands = [band1, band2, band3, band4]
 
    # Use shape of first image as reference
    target_shape = np.asarray(bands[0]).shape
    bands = [prepare_band(b, target_shape=target_shape) for b in bands]
 
    h, w = target_shape
    x = np.arange(w)
    y = np.arange(h)
    X, Y = np.meshgrid(x, y)
 
    fig = go.Figure()
 
    for i, band in enumerate(bands):
        Z = np.full((h, w), i * z_spacing, dtype=float)
 
        fig.add_trace(
            go.Surface(
                x=X,
                y=Y,
                z=Z,
                surfacecolor=band,
                cmin=0,
                cmax=1,
                colorscale="Gray",
                showscale=(i == 0),   # show colorbar only once
                opacity=opacity,
                hovertemplate=(
                    f"Band {i+1}<br>"
                    "x: %{x}<br>"
                    "y: %{y}<br>"
                    "z: %{z}<br>"
                    "intensity: %{surfacecolor:.3f}<extra></extra>"
                )
            )
        )
 
        # Add a text label beside each plane
        fig.add_trace(
            go.Scatter3d(
                x=[w + 10],
                y=[h / 2],
                z=[i * z_spacing],
                mode="text",
                text=[f"Band {i+1}"],
                showlegend=False
            )
        )
 
    fig.update_layout(
        title="3D View of 4 Image Bands",
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Band Layer",
            aspectmode="data",
            camera=dict(
                eye=dict(x=1.6, y=1.6, z=1.0)
            )
        ),
        margin=dict(l=0, r=0, t=50, b=0)
    )
 
    fig.show()
    return fig


show4(band1, band2, band3, band4, z_spacing=50, opacity=0.95)