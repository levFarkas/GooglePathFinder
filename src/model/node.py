from typing import List


class Node:
    def __init__(self, node_id, latitude=0, longitude=0, heuristics=0, city=""):
        self.node_id = node_id
        self.city = city
        self.latitude = latitude
        self.longitude = longitude
        self.heuristics = heuristics
        self.neighbor_list = []
        self.backward_neighbor_list = []

    def __hash__(self):
        return hash(self.node_id)

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.node_id == other.node_id
        return False

    def __lt__(self, other):
        return self.node_id < other.node_id

    def set_neighbors(self, l: List):
        # Shallow copies are needed to keep
        # the interconnections between the nodes
        self.neighbor_list = l

        for (n_distance, n_node) in l:
            n_node.add_backwards_neighbor([n_distance, self])

    def get_neighbors(self):
        return self.neighbor_list

    def add_backwards_neighbor(self, l: List):
        self.backward_neighbor_list.append(l)

    def get_backwards_neighbors(self):
        return self.backward_neighbor_list
