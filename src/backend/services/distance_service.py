from typing import List

from backend.persistence.connector.csv_connector import CSVConnector
from backend.persistence.connector.model.node import Node


class DistanceService:

    def __init__(self):
        self._connector = CSVConnector()

    def get_all_nodes(self) -> List[Node]:
        return self._connector.find_all()

    def get_neighbours_by_node(self, node: str) -> List[Node]:
        return self._connector.find_neighbors_by_node(node)
