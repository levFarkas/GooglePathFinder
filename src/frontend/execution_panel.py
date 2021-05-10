from multiprocessing import Pool
from random import randint
from typing import List

import dearpygui.core as core
from GooglePathFinder.src.backend.services.algorithm_handler_service import AlgorithmHandlerService
from GooglePathFinder.src.frontend.map_display import MapDisplay
from dearpygui import simple


class ExecutionPanel:
    def __init__(self, name: str, parent: str, plotter: MapDisplay):
        self.name = name
        self.parent = parent
        self.plotter = plotter
        self.algorithm_service = AlgorithmHandlerService()
        self.pool = Pool()
        self.algorithms = {
            "Dijkstra": self.algorithm_service.do_dijkstra,
            "A*": self.algorithm_service.do_astar,
            "Bidirectional A*": self.algorithm_service.do_biastar
        }
        self.available_algorithms = [*self.algorithms]
        self.selected_algorithms = []
        self.alg_result = []

    def construct(self):
        with simple.group(self.name, parent=self.parent):
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

            # GUI elements for the metrics display ################################
            core.add_radio_button("metrics",
                                  items=["Elapsed times", "Expanded nodes"],
                                  callback=self.handle_metric, 
                                  horizontal=True)
            core.add_plot("Metrics plot")
            core.add_bar_series("Metrics plot", "Metrics", [], [])
            core.set_plot_xlimits("Metrics plot", 0, 6)

    def execute_algorithms(self, sender: str, selected_algorithms: List[str]):
        init_coords = core.get_value("init_coordinate")
        dest_coords = core.get_value("destination_coordinate")

        objective = {}
        for algorithm in selected_algorithms:
            init_node = self.algorithm_service.get_nearest_node_by_lat_long(float(init_coords[0]),
                                                                            float(init_coords[1]))
            dest_node = self.algorithm_service.get_nearest_node_by_lat_long(float(dest_coords[0]),
                                                                            float(dest_coords[1]))
            objective[algorithm] = [init_node, dest_node]

        self.pool.apply_async(
            self.algorithm_service.compute,
            args=[objective],
            callback=self._handle_result
        )

    def _handle_result(self, result):
        self.plotter.refresh()
        for algorithm in result:
            route = []
            for n in algorithm["alg_result"]["path"]:
                route.append((n.latitude, n.longitude))
            self.plotter.plot_route(route, (255, 0, 0))
        self.alg_result = result
        self.handle_metric()

    def handle_metric(self):
        value = core.get_value("metrics")
        core.clear_plot("Metrics plot")

        if len(self.alg_result):
            elapsed_times = [self.alg_result[idx]["elapsed_time"] for idx in range(len(self.alg_result))]
            expanded_nodes = [algorithm["alg_result"]["expanded"] for algorithm in self.alg_result]
            bar_positions = [1, 3, 5]

            if value == 0:
                core.add_bar_series("Metrics plot", "Elapsed time", bar_positions, elapsed_times)
                core.set_plot_ylimits("Metrics plot", 0, max(elapsed_times)*1.2)
                core.configure_item("Metrics plot", x_axis_name="seconds")
            if value == 1:
                core.add_bar_series("Metrics plot", "Expanded nodes", bar_positions, expanded_nodes)
                core.set_plot_ylimits("Metrics plot", 0, max(expanded_nodes)*1.2)
                core.configure_item("Metrics plot", x_axis_name="number of nodes")


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
