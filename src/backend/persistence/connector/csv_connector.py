import csv
from typing import List

from backend.persistence.connector.interface.connector import Connector
from backend.persistence.model.node import Node


class CSVConnector(Connector):
    def find_all(self) -> List[Node]:
        with open("../resources/mocks/nodes.csv") as f:
            reader = csv.reader(f)
            data = [r for r in reader]
            header = data.pop(0)
            return [Node(dict(zip(header, row))) for row in data]

    def find_neighbors_by_node(self, node: str) -> List[Node]:
        with open("../resources/mocks/neighbours.csv") as f:
            reader = csv.reader(f)
            data = [r for r in reader]
            header = data.pop(0)
            return [Node(dict(zip(header, row))) for row in data]
