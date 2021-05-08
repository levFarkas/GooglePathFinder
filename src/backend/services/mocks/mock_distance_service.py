from typing import List, Tuple

from GooglePathFinder.src.model.node import Node
from GooglePathFinder.src.backend.services.interface.distance_interface import DistanceInterface


class MockDistanceService(DistanceInterface):
    def __init__(self):
        self.nodes = {}

    def get_all_nodes(self) -> List[Node]:
        return [n['instance'] for n in self.nodes]

    def get_neighbours_by_node(self, node: str) -> List[Node]:
        return self.nodes[node]['neighbors']

    def get_backward_neighbours_by_node(self, node: str) -> List[Node]:
        return self.nodes[node]['backward_neigbors']

    def set_neighbors(self, node: Node, l: List[Tuple[float, Node]]):
        if node.node_id not in self.nodes.keys():
            self.nodes[node.node_id] = {'instance': node, 'neighbors': [], 'backward_neigbors': []}

        self.nodes[node.node_id]['neighbors'] = l

        for (n_distance, n_node) in l:
            if n_node.node_id not in self.nodes.keys():
                self.nodes[n_node.node_id] = {'instance': n_node, 'neighbors': [], 'backward_neigbors': []}
            self.nodes[n_node.node_id]['backward_neigbors'].append([n_distance, node])
