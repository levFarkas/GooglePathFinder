from typing import List

from GooglePathFinder.src.backend.persistence.connector.model.nodedao import NodeDao


class Connector:
    def __init__(self):
        pass

    def find_all(self) -> List[NodeDao]:
        pass

    def find_neighbors_by_node(self, node: str) -> List[NodeDao]:
        pass
