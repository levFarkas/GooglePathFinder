import logging
from typing import Callable

from GooglePathFinder.src.model.node import Node


class BiAStar:
    """Bidirectional A* implementation based on the NBS algorithm
    https://arxiv.org/abs/1703.03868"""

    @staticmethod
    def run(
        start_node: Node,
        end_node: Node,
        heuristic_function: Callable[[Node, Node], float],
    ):

        solution = {
            "node": None,
            "path_cost": float("inf"),
        }

        # Forward nodes -------------------------------------------------------
        forward_dict = {
            start_node: {"sum_distance": 0, "preceding": None, "visited": True}
        }
        forward_current = start_node
        forward_open = {}
        for (n_distance, n_node) in start_node.get_neighbors():
            forward_open[n_node] = n_distance
            forward_dict[n_node] = {
                "sum_distance": n_distance,
                "preceding": start_node,
                "visited": False,
            }

            if n_node == end_node:
                solution["node"] = n_node
                solution["path_cost"] = n_distance

        # Backward nodes ------------------------------------------------------
        backward_dict = {
            end_node: {"sum_distance": 0, "preceding": None, "visited": True}
        }
        backward_current = end_node
        backward_open = {}
        for (n_distance, n_node) in end_node.get_backward_neighbors():
            backward_open[n_node] = n_distance
            backward_dict[n_node] = {
                "sum_distance": n_distance,
                "preceding": end_node,
                "visited": False,
            }

        # NBS Algorithm --------------------------------------------------------

        while len(forward_open) != 0 and len(backward_open) != 0:
            # Find candidates with minimum weight (by minimizing tentative_cost)
            min_nodes = []
            min_cost = float("inf")
            for f_node, b_node in zip(forward_open.keys(), backward_open.keys()):
                tentative_cost = max(
                    forward_open[f_node] + heuristic_function(f_node, end_node),
                    backward_open[b_node] + heuristic_function(b_node, start_node),
                    forward_open[f_node] + backward_open[b_node],
                )
                if tentative_cost < min_cost:
                    min_nodes = [(f_node, b_node)]
                    min_cost = tentative_cost
                elif tentative_cost == min_cost:
                    min_nodes.append((f_node, b_node))

            if min_cost > solution["path_cost"]:
                break

            # Expand nodes in both directions based on a forward node with minimum cost
            (f_expanded, b_expanded) = min(
                min_nodes, key=lambda node_pair: forward_open[node_pair[0]]
            )

            del forward_open[f_expanded]
            forward_dict[f_expanded]["preceding"] = forward_current
            forward_current = f_expanded
            forward_dict[forward_current]["visited"] = True

            del backward_open[b_expanded]
            backward_dict[b_expanded]["preceding"] = backward_current
            backward_current = b_expanded
            backward_dict[backward_current]["visited"] = True

            # Check the neighbors of the forward expanded node (not just in the open set)
            for (n_distance, n_node) in forward_current.get_neighbors():
                matching_backward_nodes = [
                    node for node in backward_dict.keys() if n_node == node
                ]
                neighbor_distance = (
                    forward_dict[forward_current]["sum_distance"] + n_distance
                )

                # Look for connection between forward and backward nodes
                if matching_backward_nodes:
                    assert len(matching_backward_nodes) == 1
                    path_cost = min(
                        solution["path_cost"],
                        neighbor_distance
                        + backward_dict[matching_backward_nodes[0]]["sum_distance"],
                    )
                    if path_cost < solution["path_cost"]:
                        solution = {
                            "node": n_node,
                            "path_cost": path_cost,
                        }

                # Update forward neighbors if required
                if n_node in forward_dict.keys():
                    if forward_dict[n_node]["sum_distance"] <= neighbor_distance:
                        continue

                    if forward_dict[n_node]["visited"]:
                        logging.warning("A closed node is revisited.")

                    forward_dict[n_node]["sum_distance"] = neighbor_distance
                    forward_dict[n_node]["preceding"] = forward_current
                    forward_dict[n_node]["visited"] = False
                else:
                    forward_dict[n_node] = {
                        "sum_distance": neighbor_distance,
                        "preceding": forward_current,
                        "visited": False,
                    }
                forward_open[n_node] = neighbor_distance

            # Check the neighbors of the backward expanded node (not just in the open set)
            for (n_distance, n_node) in backward_current.get_backward_neighbors():
                matching_forward_nodes = [
                    node for node in forward_dict.keys() if n_node == node
                ]
                neighbor_distance = (
                    backward_dict[backward_current]["sum_distance"] + n_distance
                )

                # Look for connection between forward and backward nodes
                if matching_forward_nodes:
                    assert len(matching_forward_nodes) == 1
                    path_cost = min(
                        solution["path_cost"],
                        neighbor_distance
                        + forward_dict[matching_forward_nodes[0]]["sum_distance"],
                    )
                    if path_cost < solution["path_cost"]:
                        solution = {
                            "node": n_node,
                            "path_cost": path_cost,
                        }

                # Update backward neighbors if required
                if n_node in backward_dict.keys():
                    if backward_dict[n_node]["sum_distance"] <= neighbor_distance:
                        continue

                    if backward_dict[n_node]["visited"]:
                        logging.warning("A closed node is revisited.")

                    backward_dict[n_node]["sum_distance"] = neighbor_distance
                    backward_dict[n_node]["preceding"] = backward_current
                    backward_dict[n_node]["visited"] = False
                else:
                    backward_dict[n_node] = {
                        "sum_distance": neighbor_distance,
                        "preceding": backward_current,
                        "visited": False,
                    }
                backward_open[n_node] = neighbor_distance

        # Evaluate the solution -----------------------------------------------
        if solution["node"] == None:
            logging.info(
                f"There is no path between {start_node.node_id} and {end_node.node_id}."
            )
            return [], float("inf")

        sum_distance = solution["path_cost"]
        logging.info(
            f"Path computed successfully between node {start_node.node_id} and \
            {end_node.node_id}. Final distance is {sum_distance}"
        )

        # Reconstruct the path
        path = []
        curr_forward = solution["node"]
        curr_backward = solution["node"]

        while curr_forward != start_node:
            path.insert(0, curr_forward.node_id)
            curr_forward = forward_dict[curr_forward]["preceding"]

        while curr_backward != None:
            curr_backward = backward_dict[curr_backward]["preceding"]
            if curr_backward != None:
                path.append(curr_backward.node_id)

        return path, sum_distance, len(backward_dict) + len(forward_dict)
