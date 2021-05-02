import math
import requests
from PIL import Image
import numpy as np
from typing import List, Type
from itertools import product


def tile_idx_generator(dimensions: int):
    base = [range(dimensions)] * 2
    permutations = list(product(*base))

    def generator():
        for i in range(len(permutations)):
            yield permutations[i][0], permutations[i][1]

    return generator


# source: https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
def deg2num(lat_deg: float, lon_deg: float, zoom: int):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)


def load_tiles(lat: float, long: float, zoom: int, num_tiles: int) -> List[int]:
    tile_x, tile_y = deg2num(lat, long, zoom)

    image_data = np.full((256 * num_tiles, 256 * num_tiles, 4), 255, dtype=np.uint8)
    idx_generator = tile_idx_generator(num_tiles)
    for x_idx, y_idx in idx_generator():
        image_url = (
            f"https://tile.openstreetmap.org/{zoom}/{tile_x+x_idx}/{tile_y+y_idx}.png"
        )

        r = requests.get(image_url, stream=True)
        if r.status_code == 200:
            data = Image.open(r.raw)
            np_image = np.asarray(data.convert("RGBA"))
            image_data[
                256 * y_idx : 256 * y_idx + 256, 256 * x_idx : 256 * x_idx + 256, :
            ] = np_image

        else:
            break
    return np.ndarray.flatten(image_data).tolist()