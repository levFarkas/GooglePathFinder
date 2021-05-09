import dearpygui.core as core
import dearpygui.simple as simple
import atexit
import os.path
from multiprocessing import Pool
from typing import List, Tuple
from numpy import save, load


from GooglePathFinder.src.frontend.image_loader import load_tiles, deg2num, num2deg


class MapDisplay:
    def __init__(
        self,
        name: str,
        parent: str,
        tile_radius: int,
        latitude: float,
        longitude: float,
    ):
        self.name = name
        self.parent = parent
        self.tile_radius = tile_radius
        self.latitude = latitude
        self.longitude = longitude
        self.zoom = 15
        self.pool = Pool()
        self.map_size = [700, 700]
        self.stored_map = [255 for i in range(self.map_size[0] * self.map_size[1] * 4)]
        self.cached = False

        if os.path.exists("cached_map.npy"):
            self.stored_map = load("cached_map.npy")
            self.cached = True

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

    def pixel_to_coordinate(self, percent_x: float, percent_y: float):
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

    def coordinate_to_pixel(self, latitude: float, longitude: float):
        self.adjust_coordinate_to_center_tile()
        x_tile, y_tile = deg2num(self.latitude, self.longitude, self.zoom)
        lat_next, long_next = num2deg(x_tile + 1, y_tile - 1, self.zoom)

        lat_delta = lat_next - self.latitude
        long_delta = long_next - self.longitude

        lat_first = self.latitude - (self.tile_radius + 1) * lat_delta
        long_first = self.longitude - self.tile_radius * long_delta

        lat_last = lat_first + (2 * self.tile_radius + 1) * lat_delta
        long_last = long_first + (2 * self.tile_radius + 1) * long_delta

        return ((longitude - long_first) / (long_last - long_first)), (
            (latitude - lat_first) / (lat_last - lat_first)
        )

    def plot_route(self, route: List[Tuple[float, float]], route_color=(255, 50, 50)):
        transformed = [self.coordinate_to_pixel(p[0], p[1]) for p in route]
        p_x = [int(self.map_size[0] * t[0]) for t in transformed]
        p_y = [self.map_size[1] - int(self.map_size[1] * t[1]) for t in transformed]
        for i in range(1, len(route)):
            core.draw_line(
                "canvas",
                [p_x[i - 1], p_y[i - 1]],
                [p_x[i], p_y[i]],
                color=route_color,
                thickness=3,
            )

    def construct(self):
        self.adjust_coordinate_to_center_tile()
        with simple.group(self.name, parent=self.parent):
            core.add_drawing("canvas", width=self.map_size[0], height=self.map_size[1])
            core.add_texture(
                "geomap",
                self.stored_map,
                256 * self.tile_radius,
                256 * self.tile_radius,
            )

            if self.cached == False:
                # Only use if necessary so that the OSM tile servers are not overloaded.
                self.async_update_by_coordinate(
                    self.latitude, self.longitude, self.zoom
                )
            else:
                self.refresh()

    def async_update_by_coordinate(self, latitude: float, longitude: float, zoom: int):
        self.pool.apply_async(
            load_tiles,
            kwds={
                "lat": latitude,
                "long": longitude,
                "zoom": zoom,
                "tile_radius": self.tile_radius,
            },
            callback=self.update,
        )

    def update(self, image_data: List[float]):
        self.stored_map = image_data
        save("cached_map.npy", image_data)
        self.cached = True
        self.refresh()

    def refresh(self):
        core.add_texture(
            "geomap",
            self.stored_map,
            256 * (2 * self.tile_radius + 1),
            256 * (2 * self.tile_radius + 1),
        )
        core.draw_image("canvas", "geomap", [0, 0], self.map_size)
