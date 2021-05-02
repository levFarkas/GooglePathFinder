import dearpygui.core as core
import dearpygui.simple as simple
import atexit
from multiprocessing import Pool

from GooglePathFinder.src.frontend.image_loader import load_tiles


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
            map_display = MapDisplay("map_display", parent="main_panel", num_tiles=4)
            map_display.construct()

            core.add_group("user_panel", parent="main_panel", horizontal=False)
            input_panel = InputPanel("input_panel", parent="user_panel")
            input_panel.construct()

            execution_panel = ExecutionPanel("execution_panel", parent="user_panel")
            execution_panel.construct()
            core.end()  # user_panel

            core.end()  # main_panel

    @staticmethod
    def run():
        core.start_dearpygui(primary_window="main_window")


class MapDisplay:
    def __init__(self, name, parent, num_tiles):
        self.name = name
        self.parent = parent
        self.num_tiles = num_tiles
        self.pool = Pool()

        def destruct():
            self.pool.terminate()
            self.pool.join()

        atexit.register(destruct)

    def construct(self):
        with simple.group(self.name, parent=self.parent):
            core.add_drawing("canvas", width=700, height=700)
            core.add_texture(
                "geomap",
                [255 for i in range(700 * 700 * 4)],
                256 * self.num_tiles,
                256 * self.num_tiles,
            )

            self.async_update_by_coordinate(46.98828541972894, 17.933220574578318, 16)

    def async_update_by_coordinate(self, lat, long, zoom):
        self.pool.apply_async(
            load_tiles,
            kwds={
                "lat": lat,
                "long": long,
                "zoom": zoom,
                "num_tiles": self.num_tiles,
            },
            callback=self.update,
        )

    def update(self, image_data):
        core.add_texture(
            "geomap",
            image_data,
            256 * self.num_tiles,
            256 * self.num_tiles,
        )
        core.draw_image("canvas", "geomap", [0, 0], [700, 700])


class InputPanel:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent

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

    def sample_by_mouse(self, sender, callback_object):
        def update_on_click(sender):
            core.set_value(callback_object, core.get_drawing_mouse_pos())
            core.set_mouse_click_callback(None)

        core.set_mouse_click_callback(update_on_click)


class ExecutionPanel:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent

    def construct(self):
        pass