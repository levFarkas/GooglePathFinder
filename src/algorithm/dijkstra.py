import logging
from queue import PriorityQueue

from GooglePathFinder.src.model.node import Node


class Dijkstra:
    @staticmethod
    def run(start_node: Node, end_node: Node):
        curr_node = start_node
        curr_distance = 0

        node_dict = {curr_node: {"sum_distance": 0, "preceding": None, "visited": True}}

        # Nodes may appear multiple times in the queue, since the update of priorities is not
        # supported in queue.PriorityQueue. Instead, the invalid queue elements are skipped.
        # A node is invalid if the queued distance does not match the stored distance.

        neighbor_queue = PriorityQueue()
        for (n_distance, n_node) in start_node.get_neighbors():
            neighbor_queue.put([n_distance, n_node])
            node_dict[n_node] = {
                "sum_distance": n_distance,
                "preceding": curr_node,
                "visited": False,
            }

        while curr_node != end_node and not neighbor_queue.empty():
            curr_distance, curr_node = neighbor_queue.get()

            # Skip invalid nodes
            if node_dict[curr_node]["sum_distance"] != curr_distance:
                continue

            node_dict[curr_node]["visited"] = True

            for (n_distance, n_node) in curr_node.get_neighbors():
                updated_distance = curr_distance + n_distance

                if n_node not in node_dict.keys():
                    queued_node = [updated_distance, n_node]
                    neighbor_queue.put(queued_node)
                    node_dict[n_node] = {
                        "sum_distance": updated_distance,
                        "preceding": curr_node,
                        "visited": False,
                    }

                elif node_dict[n_node]["sum_distance"] > updated_distance:
                    if node_dict[n_node]["visited"]:
                        raise AssertionError(
                            "The fetched node is already visited but the path is not optimal!"
                        )

                    queued_node = [updated_distance, n_node]
                    neighbor_queue.put(queued_node)
                    node_dict[n_node]["preceding"] = curr_node
                    node_dict[n_node]["sum_distance"] = updated_distance

        # Evaluate the solution ------------------------------------------------
        if curr_node != end_node:
            logging.info(
                f"There is no path between {start_node.node_id} and {end_node.node_id}."
            )
            return [], float("inf")

        sum_distance = node_dict[end_node]["sum_distance"]
        logging.info(
            f"Path computed successfully between node {start_node.node_id} and {end_node.node_id}. Final distance is {sum_distance}"
        )
        path = []
        while curr_node != start_node:
            path.insert(0, curr_node.node_id)
            curr_node = node_dict[curr_node]["preceding"]

        return path, sum_distance