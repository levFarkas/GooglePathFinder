from GooglePathFinder.src.backend.services.distance_service import DistanceService
from GooglePathFinder.src.frontend.pathfinder_gui import PathFinderGui


class Handler:
    def __init__(self):
        self._distance_service = DistanceService()

    # Main function
    def handle(self, config=None):
        pass


if __name__ == "__main__":
    handler = Handler()
    handler.handle()

    gui = PathFinderGui(1180, 720)
    gui.construct()
    gui.run()
