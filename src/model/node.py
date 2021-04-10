from typing import List


class Node:
    def __init__(self, node_id, city="", latitude=0, longitude=0, heuristics=0):
        self.node_id = node_id
        self.city = city
        self.latitude = latitude
        self.longitude = longitude
        self.heuristics = heuristics
        self.neighbor_list = []

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

    def get_neighbors(self):
        return self.neighbor_list
