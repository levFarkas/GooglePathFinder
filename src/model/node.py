from typing import List

class Node:
    def __init__(self, node_id, latitude=0, longitude=0, heuristics=0, city=""):
        self.node_id = node_id
        self.city = city
        self.latitude = latitude
        self.longitude = longitude
        self.heuristics = heuristics

    def __hash__(self):
        return hash(self.node_id)

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.node_id == other.node_id
        return False

    def __lt__(self, other):
        return self.node_id < other.node_id
