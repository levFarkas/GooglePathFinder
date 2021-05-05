from multiprocessing import Process
from multiprocessing import Queue
from typing import List, Dict

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
    def do_dijkstra(self):
        return []
        # return Dijkstra.run()

    @metric_measure
    def do_astar(self):
        return []
        # return AStar.run()

    @metric_measure
    def do_biastar(self):
        return []
        # return BiAStar.run()

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
