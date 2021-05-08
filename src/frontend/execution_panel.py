from multiprocessing import Pool
from typing import List

import dearpygui.core as core

from GooglePathFinder.src.backend.services.algorithm_handler_service import AlgorithmHandlerService


class ExecutionPanel:
    def __init__(self, name: str, parent: str):
        self.name = name
        self.parent = parent
        self.algorithm_service = AlgorithmHandlerService()
        self.pool = Pool()
        self.algorithms = {
            "Dijkstra": self.algorithm_service.do_dijkstra,
            "A*": self.algorithm_service.do_astar,
            "Bidirectional A*": self.algorithm_service.do_biastar
        }
        self.available_algorithms = [*self.algorithms]
        self.selected_algorithms = []

    def construct(self):
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
        core.add_button(
            "Execute",
            callback=self.execute_algorithms,
            callback_data=self.selected_algorithms,
        )

    def execute_algorithms(self, sender: str, selected_algorithms: List[str]):
        init_coords = core.get_value("init_coordinate")
        dest_coords = core.get_value("destination_coordinate")

        for algorithm in selected_algorithms:
            result = self.pool.apply_async(
                self._do_execute,
                args=[algorithm, init_coords, dest_coords],
                callback=self._handle_result
            )
            result.get()

    def _do_execute(self, algorithm: str, init_coords, dest_coords):
        init_node = self.algorithm_service.get_nearest_node_by_lat_long(float(init_coords[0]), float(init_coords[1]))
        dest_node = self.algorithm_service.get_nearest_node_by_lat_long(float(dest_coords[0]), float(dest_coords[1]))
        print(init_node.node_id)
        print(dest_node.node_id)
        return self.algorithms[algorithm](init_node, dest_node)

    def _handle_result(self, result):
        print(result)

    def update_listbox(self):
        core.configure_item(
            "algorithm_selector##available", items=self.available_algorithms
        )
        core.set_value("algorithm_selector##available", 0)
        core.configure_item(
            "algorithm_selector##selected", items=self.selected_algorithms
        )
        core.set_value("algorithm_selector##selected", 0)

    def __getstate__(self):
        self_dict = self.__dict__.copy()
        del self_dict['pool']
        return self_dict

    def __setstate__(self, state):
        self.__dict__.update(state)