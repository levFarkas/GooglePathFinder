import dearpygui.core as core
import dearpygui.simple as simple

from GooglePathFinder.src.frontend.map_display import MapDisplay
from GooglePathFinder.src.frontend.input_panel import InputPanel
from GooglePathFinder.src.frontend.execution_panel import ExecutionPanel


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
