from typing import List

from backend.persistence.model.node import Node


class Connector:
    def __init__(self):
        pass

    def find_all(self) -> List[Node]:
        pass

    def find_neighbors_by_node(self, node: str) -> List[Node]:
        pass
