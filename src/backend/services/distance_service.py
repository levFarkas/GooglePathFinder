from typing import List, Tuple

from GooglePathFinder.src.backend.persistence.connector.mysql_connector import MySQLConnector
from GooglePathFinder.src.backend.services.interface.distance_interface import DistanceInterface
from GooglePathFinder.src.backend.persistence.connector.csv_connector import CSVConnector
from GooglePathFinder.src.model.node import Node


class DistanceService(DistanceInterface):

    def __init__(self):
        self._connector = CSVConnector()

    def get_all_nodes(self) -> List[Node]:
        node_daos = self._connector.find_all()
        nodes = [nodedao.convert_to_node_model() for nodedao in node_daos]
        return nodes

    def get_neighbours_by_node(self, node: str) -> List[Tuple[float, Node]]:
        node_daos = self._connector.find_neighbors_by_node(node)
        nodes = [(nodedao.distance, nodedao.convert_to_node_model()) for nodedao in node_daos]
        return nodes

    def get_backward_neighbours_by_node(self, node: str) -> List[Tuple[float, Node]]:
        node_daos = self._connector.find_backward_neighbors_by_node(node)
        nodes = [(nodedao.distance, nodedao.convert_to_node_model()) for nodedao in node_daos]
        return nodes
