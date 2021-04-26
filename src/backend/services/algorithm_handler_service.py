from src.backend.services.distance_service import DistanceService


class Alg:

    def __init__(self):
        self._distance_service = DistanceService()

    def doAstar(self, start_node, end_node) -> Result:
        self._distance_service.get_all_nodes()
        Astar()