import csv
from typing import List

from backend.persistence.connector.interface.connector import Connector
from backend.persistence.connector.model.node import Node


class CSVConnector(Connector):
    def find_all(self) -> List[Node]:
        with open("../resources/mocks/nodes.csv") as f:
            return self._read_data(f)

    def find_neighbors_by_node(self, node: str) -> List[Node]:
        with open("../resources/mocks/neighbours.csv") as f:
            return self._read_data

    @staticmethod
    def _read_data(f):
        reader = csv.reader(f)
        data = [r for r in reader]
        header = data.pop(0)
        return [Node(dict(zip(header, row))) for row in data]
