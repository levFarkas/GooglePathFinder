from typing import List

from GooglePathFinder.src.model.node import Node


class DistanceInterface:

    def __init__(self):
        pass

    def get_all_nodes(self) -> List[Node]:
        pass

    def get_neighbours_by_node(self, node: str) -> List[Node]:
        pass

    def get_backward_neighbours_by_node(self, node: str) -> List[Node]:
        pass
