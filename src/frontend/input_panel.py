import dearpygui.core as core
import dearpygui.simple as simple


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
