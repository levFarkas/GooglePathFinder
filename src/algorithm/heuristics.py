import math
from geopy import distance
from geopy import Point

from GooglePathFinder.src.model.node import Node


def l2distance(x, y):
    return math.sqrt(sum([pow(i - j, 2) for (i, j) in zip(x, y)]))


# latitude and longitude are treated as cartesian coordinates (only for testing purposes!)
def node_l2distance(node_x: Node, node_y: Node):
    return l2distance(
        (node_x.latitude, node_x.longitude), (node_y.latitude, node_y.longitude)
    )


def node_shperical_distance(node_x: Node, node_y, Node):
    p1 = Point(latitude=node_x.latitude, longitude=node_x.longitude)
    p2 = Point(latitude=node_y.latitude, longitude=node_y.longitude)
    return distance.distance(p1, p2).meters
