import dearpygui.core as core
import dearpygui.simple as simple


class PathFinderGui:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def construct(self):
        core.set_main_window_title("Pathfinder")
        core.set_main_window_pos(0, 0)
        core.set_main_window_size(width=self.width, height=self.height)
        core.set_main_window_resizable(resizable=False)

        with simple.window("Main Window"):
            core.add_group("main")
            core.end()

    @staticmethod
    def run():
        core.start_dearpygui(primary_window="Main Window")
