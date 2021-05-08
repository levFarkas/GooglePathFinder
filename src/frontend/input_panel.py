from typing import List

import dearpygui.core as core
import dearpygui.simple as simple

from GooglePathFinder.src.frontend.map_display import MapDisplay


class InputPanel:
    def __init__(self, name: str, parent: str, map_display: MapDisplay):
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


    def sample_by_mouse(self, sender: str, callback_object: str):
        def update_on_click(sender):
            pos_x, pos_y = core.get_drawing_mouse_pos()
            sx, sy = self.context.get_drawing_size()
            coordinates = self.context.pixel_to_coordinate(
                pos_x / sx, (sy - pos_y) / sy
            )
            print(coordinates)
            core.set_value(callback_object, coordinates)
            core.set_mouse_click_callback(None)

        core.set_mouse_click_callback(update_on_click)

