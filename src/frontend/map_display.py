import dearpygui.core as core
import dearpygui.simple as simple
import atexit
from multiprocessing import Pool

from GooglePathFinder.src.frontend.image_loader import load_tiles, deg2num, num2deg


class MapDisplay:
    def __init__(self, name, parent, tile_radius, latitude, longitude):
        self.name = name
        self.parent = parent
        self.tile_radius = tile_radius
        self.latitude = latitude
        self.longitude = longitude
        self.zoom = 16
        self.pool = Pool()
        self.map_size = [700, 700]

        def destruct():
            self.pool.terminate()
            self.pool.join()

        atexit.register(destruct)

    def get_drawing_size(self):
        return self.map_size

    def adjust_coordinate_to_center_tile(self):
        x_tile, y_tile = deg2num(self.latitude, self.longitude, self.zoom)
        lat_adjusted, long_adjusted = num2deg(x_tile, y_tile, self.zoom)
        self.latitude = lat_adjusted
        self.longitude = long_adjusted

    def convert_map_coordinate(self, percent_x, percent_y):
        self.adjust_coordinate_to_center_tile()
        x_tile, y_tile = deg2num(self.latitude, self.longitude, self.zoom)
        lat_next, long_next = num2deg(x_tile + 1, y_tile - 1, self.zoom)

        lat_delta = lat_next - self.latitude
        long_delta = long_next - self.longitude

        lat_first = self.latitude - (self.tile_radius + 1) * lat_delta
        long_first = self.longitude - self.tile_radius * long_delta

        lat_current = lat_first + (2 * self.tile_radius + 1) * lat_delta * percent_y
        long_current = long_first + (2 * self.tile_radius + 1) * long_delta * percent_x

        return lat_current, long_current

    def construct(self):
        self.adjust_coordinate_to_center_tile()
        with simple.group(self.name, parent=self.parent):
            core.add_drawing("canvas", width=self.map_size[0], height=self.map_size[1])
            core.add_texture(
                "geomap",
                [255 for i in range(self.map_size[0] * self.map_size[1] * 4)],
                256 * self.tile_radius,
                256 * self.tile_radius,
            )

            self.async_update_by_coordinate(self.latitude, self.longitude, self.zoom)

    def async_update_by_coordinate(self, lat, long, zoom):
        self.pool.apply_async(
            load_tiles,
            kwds={
                "lat": lat,
                "long": long,
                "zoom": zoom,
                "tile_radius": self.tile_radius,
            },
            callback=self.update,
        )

    def update(self, image_data):
        core.add_texture(
            "geomap",
            image_data,
            256 * (2 * self.tile_radius + 1),
            256 * (2 * self.tile_radius + 1),
        )
        core.draw_image("canvas", "geomap", [0, 0], self.map_size)
