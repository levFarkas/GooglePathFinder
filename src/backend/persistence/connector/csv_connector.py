import csv
from typing import List, Optional

from GooglePathFinder.src.backend.persistence.connector.interface.connector import Connector
from GooglePathFinder.src.backend.persistence.connector.model.nodedao import NodeDao


class CSVConnector(Connector):
    def find_all(self) -> List[NodeDao]:
        with open("../resources/mocks/nodes.csv") as f:
            return self._read_data(f)

    def find_node_by_id(self, node : str) -> Optional[NodeDao]:
        with open("../resources/mocks/nodes.csv") as f:
            for n in self._read_data(f):
                if n.node_id == node: return n
            return None

    def find_neighbors_by_node(self, node: str) -> List[NodeDao]:
        with open("../resources/mocks/neighbours.csv") as f:
            return self._read_data(f)

    def find_backward_neighbors_by_node(self, node: str) -> List[NodeDao]:
        with open("../resources/mocks/backward_neighbours.csv") as f:
            return self._read_data(f)

    @staticmethod
    def _read_data(f):
        reader = csv.reader(f)
        data = [r for r in reader]
        header = data.pop(0)
        return [NodeDao(dict(zip(header, row))) for row in data]