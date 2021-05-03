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
                latitude=47.48460625322428,
                longitude=19.052776677264482,
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


class InputPanel:
    def __init__(self, name, parent, map_display):
        self.name = name
        self.parent = parent
        self.context = map_display
        self.available_algorithms = ["Dijkstra", "A*", "Bidirectional A*"]
        self.selected_algorithms = []

    def construct(self):
        with simple.group(self.name, parent=self.parent):
            # GUI elements for the initial coordinate #########################
            core.add_text("Initial coordinate (latitude, longitude)")
            core.add_group("init_input", horizontal=True, horizontal_spacing=0)
            core.add_input_float2("init_coordinate", label="", format="%f°", width=390)
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
                "destination_coordinate", format="%f°", label="", width=390
            )
            core.add_button(
                "Sample##destination",
                callback=self.sample_by_mouse,
                callback_data=("destination_coordinate"),
            )
            core.end()  # destination_input

            core.add_spacing(count=5)

            # GUI elements for the algorithm selection ########################
            core.add_group(
                "algorithm_input##labels", horizontal=True, horizontal_spacing=90
            )
            core.add_text("Available algorithms")
            core.add_text("Selected algorithms")
            core.end()  # algorithm_input##labels

            core.add_group(
                "algorithm_input#lists", horizontal=True, horizontal_spacing=0
            )
            core.add_listbox(
                "algorithm_selector##available",
                label="",
                items=self.available_algorithms,
                width=220,
            )
            core.add_listbox(
                "algorithm_selector##selected",
                label="",
                items=self.selected_algorithms,
                width=220,
            )
            core.end()  # algorithm_input##lists

            def move(src, dest, gui_element):
                if len(src):
                    current = core.get_value(gui_element)
                    item = src.pop(current)
                    dest.append(item)
                    self.update_listbox()

            def move_all(src, dest):
                for i in src:
                    dest.append(i)
                src.clear()
                self.update_listbox()

            def add(sender):
                move(
                    self.available_algorithms,
                    self.selected_algorithms,
                    "algorithm_selector##available",
                )

            def add_all(sender):
                move_all(self.available_algorithms, self.selected_algorithms)

            def remove(sender):
                move(
                    self.selected_algorithms,
                    self.available_algorithms,
                    "algorithm_selector##selected",
                )

            def remove_all(sender):
                move_all(self.selected_algorithms, self.available_algorithms)

            core.add_group("algorithm_input##buttons", horizontal=True)
            core.add_button("Add", width=107, callback=add)
            core.add_button("Add all", width=107, callback=add_all)
            core.add_button("Remove", width=107, callback=remove)
            core.add_button("Remove all", width=107, callback=remove_all)
            core.end()  # algorithm_input##buttons

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

    def update_listbox(self):
        core.configure_item(
            "algorithm_selector##available", items=self.available_algorithms
        )
        core.set_value("algorithm_selector##available", 0)
        core.configure_item(
            "algorithm_selector##selected", items=self.selected_algorithms
        )
        core.set_value("algorithm_selector##selected", 0)


class ExecutionPanel:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent

    def construct(self):
        pass