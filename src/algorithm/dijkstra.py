import logging
from queue import PriorityQueue
from copy import deepcopy

from GooglePathFinder.src.model.node import Node
from GooglePathFinder.src.backend.services.interface.distance_interface import DistanceInterface


class Dijkstra:
    """Dijkstra algorithm using a priority queue. Nodes may appear multiple times in
    the queue, since the update of priorities is not supported in queue.PriorityQueue.
    Instead, the invalid queue elements are skipped. A node is invalid if the queued
    distance does not match the separately stored distance."""

    @staticmethod
    def run(start_node: Node, end_node: Node, distance_service: DistanceInterface):

        curr_node = start_node
        curr_distance = 0

        node_dict = {curr_node: {"sum_distance": 0, "preceding": None, "visited": True}}

        neighbor_queue = PriorityQueue()
        for (n_distance, n_node) in distance_service.get_neighbours_by_node(start_node.node_id):
            neighbor_queue.put([n_distance, n_node])
            node_dict[n_node] = {
                "sum_distance": n_distance,
                "preceding": deepcopy(curr_node),
                "visited": False,
            }

        while curr_node != end_node and not neighbor_queue.empty():
            curr_distance, curr_node = neighbor_queue.get()

            # Skip invalid nodes
            if node_dict[curr_node]["sum_distance"] != curr_distance:
                continue

            node_dict[curr_node]["visited"] = True

            for (n_distance, n_node) in distance_service.get_neighbours_by_node(curr_node.node_id):
                updated_distance = curr_distance + n_distance

                if n_node not in node_dict.keys():
                    neighbor_queue.put([updated_distance, n_node])
                    node_dict[n_node] = {
                        "sum_distance": updated_distance,
                        "preceding": deepcopy(curr_node),
                        "visited": False,
                    }

                elif node_dict[n_node]["sum_distance"] > updated_distance:
                    if node_dict[n_node]["visited"]:
                        raise AssertionError(
                            "The fetched node is already visited but the path is not optimal!"
                        )

                    neighbor_queue.put([updated_distance, n_node])
                    node_dict[n_node]["preceding"] = deepcopy(curr_node)
                    node_dict[n_node]["sum_distance"] = updated_distance

        # Evaluate the solution ------------------------------------------------
        if curr_node != end_node:
            return {"path": [], "distance": float("inf"), "expanded": len(node_dict)}

        sum_distance = node_dict[end_node]["sum_distance"]

        # Reconstruct the path
        path = []
        while curr_node != start_node:
            path.insert(0, deepcopy(curr_node))
            curr_node = node_dict[curr_node]["preceding"]

        return {"path": path, "distance": sum_distance, "expanded": len(node_dict)}
