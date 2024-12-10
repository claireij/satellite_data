from pyproj import Proj, transform
import numpy as np
from PIL import Image
from io import BytesIO

def transform_coordinates(dataset):
    src_proj = Proj("epsg:32633")
    dest_proj = Proj("epsg:4326")
    left, bottom, right, top = dataset.bounds
    south_west = transform(src_proj, dest_proj, left, bottom)
    north_east = transform(src_proj, dest_proj, right, top)
    return south_west, north_east

def generate_image_from_raster(raster_data):
    normalized_data = ((raster_data - raster_data.min()) / 
                       (raster_data.max() - raster_data.min()) * 255).astype(np.uint8)
    image = Image.fromarray(normalized_data, mode="L")
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer
