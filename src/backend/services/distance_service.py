from typing import List

from GooglePathFinder.src.backend.persistence.connector.csv_connector import CSVConnector
from GooglePathFinder.src.model.node import Node


class DistanceService:

    def __init__(self):
        self._connector = CSVConnector()

    def get_all_nodes(self) -> List[Node]:
        node_daos = self._connector.find_all()
        nodes = [Node(
            node_id=nodedao.id,
            longitude=nodedao.longitude,
            latitude=nodedao.latitude,
            heuristics=nodedao.heuristic,
            city=nodedao.city
        ) for nodedao in node_daos]
        return nodes

    def get_neighbours_by_node(self, node: str) -> List[Node]:
        node_daos = self._connector.find_neighbors_by_node(node)
        nodes = [Node(
            node_id=nodedao.id,
            longitude=nodedao.longitude,
            latitude=nodedao.latitude,
            heuristics=nodedao.heuristic,
            city=nodedao.city
        ) for nodedao in node_daos]
        return nodes
