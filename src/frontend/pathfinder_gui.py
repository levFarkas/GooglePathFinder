import dearpygui.core as core
import dearpygui.simple as simple
import atexit
from multiprocessing import Pool

from GooglePathFinder.src.frontend.image_loader import load_tiles, deg2num, num2deg


class PathFinderGui:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def construct(self):
        core.set_main_window_title("Pathfinder")
        core.set_main_window_pos(0, 0)
        core.set_main_window_size(width=self.width, height=self.height)
        core.set_main_window_resizable(resizable=False)

        with simple.window("main_window"):
            core.add_group("main_panel", parent="main_window", horizontal=True)
            # MapDisplay ######################################################
            map_display = MapDisplay(
                "map_display",
                parent="main_panel",
                tile_radius=1,
                latitude=46.98337006427196,
                longitude=17.94085796579044,
            )
            map_display.construct()

            # InputPanel ######################################################
            core.add_group("user_panel", parent="main_panel", horizontal=False)
            input_panel = InputPanel(
                "input_panel", parent="user_panel", map_display=map_display
            )
            input_panel.construct()

            execution_panel = ExecutionPanel("execution_panel", parent="user_panel")
            execution_panel.construct()
            core.end()  # user_panel

            ###################################################################
            core.end()  # main_panel

    @staticmethod
    def run():
        core.start_dearpygui(primary_window="main_window")


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

    def adjust_coordinate_to_center_block(self):
        x_tile, y_tile = deg2num(self.latitude, self.longitude, self.zoom)
        lat_adjusted, long_adjusted = num2deg(x_tile, y_tile, self.zoom)
        self.latitude = lat_adjusted
        self.longitude = long_adjusted

    def convert_map_coordinate(self, percent_x, percent_y):
        self.adjust_coordinate_to_center_block()
        x_tile, y_tile = deg2num(self.latitude, self.longitude, self.zoom)
        lat_next, long_next = num2deg(x_tile + 1, y_tile + 1, self.zoom)

        lat_delta = self.latitude - lat_next
        long_delta = long_next - self.longitude

        lat_first = self.latitude - (self.tile_radius + 1) * lat_delta
        long_first = self.longitude - self.tile_radius * long_delta

        return (lat_first + (2 * self.tile_radius + 1) * lat_delta * (percent_y)), (
            long_first + (2 * self.tile_radius + 1) * long_delta * percent_x
        )

    def construct(self):
        self.adjust_coordinate_to_center_block()
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


class InputPanel:
    def __init__(self, name, parent, map_display):
        self.name = name
        self.parent = parent
        self.context = map_display

    def construct(self):
        with simple.group(self.name, parent=self.parent):
            # GUI elements for the initial coordinate #########################
            core.add_text("Initial coordinate (latitude, longitude)")
            core.add_group("init_input", horizontal=True, horizontal_spacing=0)
            core.add_input_float2("init_coordinate", label="", format="%f°", width=450)
            core.add_button(
                "Sample##input",
                callback=self.sample_by_mouse,
                callback_data=("init_coordinate"),
            )
            core.end()  # init_input

            core.add_spacing(count=5)

            # GUI elements for the destination coordinate #####################
            core.add_text("Destination coordinate (latitude, longitude)")
            core.add_group("destination_input", horizontal=True, horizontal_spacing=0)
            core.add_input_float2(
                "destination_coordinate", format="%f°", label="", width=450
            )
            core.add_button(
                "Sample##destination",
                callback=self.sample_by_mouse,
                callback_data=("destination_coordinate"),
            )
            core.end()  # destination_input

            core.add_spacing(count=5)

            # GUI elements for the algorithm selection ########################
            core.add_text("Algorithm selection")
            core.add_listbox(
                "algorithm_selector",
                label="",
                items=["Dijkstra", "A*", "Bidirectional A*"],
                width=450,
            )

    def sample_by_mouse(self, sender, callback_object):
        def update_on_click(sender):
            pos_x, pos_y = core.get_drawing_mouse_pos()
            sx, sy = self.context.get_drawing_size()
            coordinates = self.context.convert_map_coordinate(
                pos_x / sx, (sy - pos_y) / sy
            )
            core.set_value(callback_object, coordinates)
            core.set_mouse_click_callback(None)

        core.set_mouse_click_callback(update_on_click)


class ExecutionPanel:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent

    def construct(self):
        pass