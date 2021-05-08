from functools import reduce
from multiprocessing import Process
from multiprocessing import Queue
from typing import List, Dict

from GooglePathFinder.src.algorithm.heuristics import l2distance, node_l2distance
from GooglePathFinder.src.backend.services.distance_service import DistanceService
from GooglePathFinder.src.algorithm.dijkstra import Dijkstra
from GooglePathFinder.src.algorithm.astar import AStar
from GooglePathFinder.src.algorithm.bi_astar import BiAStar
from GooglePathFinder.src.backend.adapter.metric_measure import metric_measure
from GooglePathFinder.src.model.node import Node


class AlgorithmHandlerService:
    def __init__(self):
        self.distance_service = DistanceService()

    @metric_measure
    def do_dijkstra(self, start_node: Node, end_node: Node):
        return Dijkstra.run(start_node, end_node)

    @metric_measure
    def do_astar(self, start_node: Node, end_node: Node):
        return AStar.run(start_node, end_node, node_l2distance)

    @metric_measure
    def do_biastar(self, start_node: Node, end_node: Node):
        return BiAStar.run(start_node, end_node, node_l2distance)

    @staticmethod
    def _min(a, b):
        return a if a["distance"] < b["distance"] else b

    def get_nearest_node_by_lat_long(self, lat, long):
        nodes = self.distance_service.get_all_nodes()
        nodes_distances = [
            {
                "node": node,
                "distance": l2distance([lat, long], [float(node.latitude), float(node.longitude)])
            } for node in nodes
        ]
        return reduce(self._min, nodes_distances)["node"]

    def algorithm_mapper(self, algorithm_id: str):
        if algorithm_id == "dijkstra":
            return self.do_dijkstra()

        if algorithm_id == "astar":
            return self.do_astar()

        if algorithm_id == "biastar":
            return self.do_biastar()

    def compute(self, objective: Dict, algorithms: List):
        """Call this function using a multiprocessing pool"""
        self.objective = objective
        self.algorithms = algorithms

        try:
            return map(self.algorithm_mapper, self.algorithms)
        except:
            return []
