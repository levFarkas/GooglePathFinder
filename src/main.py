import logging
from GooglePathFinder.src.backend.services.distance_service import DistanceService
from GooglePathFinder.src.frontend.pathfinder_gui import PathFinderGui

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    gui = PathFinderGui(1180, 720)
    gui.construct()
    gui.run()
