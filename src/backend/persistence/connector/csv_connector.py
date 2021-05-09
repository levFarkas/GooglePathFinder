import csv
import logging
from typing import List, Optional

from GooglePathFinder.src.backend.persistence.connector.interface.connector import Connector
from GooglePathFinder.src.backend.persistence.connector.model.nodedao import NodeDao


class CSVConnector(Connector):
    def __init__(self):
        self.loaded_data = []
        self.loaded_edges = []

    def find_all(self) -> List[NodeDao]:
        if len(self.loaded_data):
            return self.loaded_data
        with open("../resources/offline_dataset/nodes.csv") as f:
            self.loaded_data = self._read_nodes(f)
            return self.loaded_data

    def find_all_edges(self):
        if len(self.loaded_edges):
            return self.loaded_edges
        with open("../resources/offline_dataset/edges.csv") as f:
            self.loaded_edges = self._read_edges(f)
            return self.loaded_edges

    def find_node_by_id(self, node : str) -> Optional[NodeDao]:
        for n in self.find_all():
            if n.node_id == node: return n
        return None

    def find_neighbors_by_node(self, node: str) -> List[NodeDao]:
        edges = self.find_all_edges()
        neighbor_entries = [(edge["TO_ID"], edge["DISTANCE"]) for edge in edges if edge["FROM_ID"] == node]
        return self._create_neighbor_list(neighbor_entries)
            

    def find_backward_neighbors_by_node(self, node: str) -> List[NodeDao]:
        edges = self.find_all_edges()
        neighbor_entries = [(edge["FROM_ID"], edge["DISTANCE"]) for edge in edges if edge["TO_ID"] == node]
        return self._create_neighbor_list(neighbor_entries)

    
    def _create_neighbor_list(self,neighbor_entries: list):
        neighbors = []
        for n in neighbor_entries:
            current_dao = self.find_node_by_id(n[0])
            if current_dao is None:
                continue
            current_dao.distance = float(n[1])
            neighbors.append(current_dao)
        return neighbors


    @staticmethod
    def _read_nodes(f):
        reader = csv.reader(f)
        data = [r for r in reader]
        header = data.pop(0)
        return [NodeDao(dict(zip(header, row))) for row in data]

    @staticmethod
    def _read_edges(f):
        reader = csv.reader(f)
        data = [r for r in reader]
        header = data.pop(0)
        return [dict(zip(header, row)) for row in data]