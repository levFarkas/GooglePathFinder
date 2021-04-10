from GooglePathFinder.src.model.node import Node
from queue import PriorityQueue


class Dijkstra:
    @staticmethod
    def run(start_node: Node, end_node: Node):
        curr_node = start_node

        # Store distance values and preceding node in a dictionary.
        # Elements of the priority queue are stored separately as well
        # to quickly update the distances without iterating through the queue.
        # Unvisited nodes are not present.

        node_dict = {
            curr_node: {"sum_distance": 0, "preceding": None, "queue_ref": None}
        }

        neighbor_queue = PriorityQueue()
        for n in start_node.get_neighbors():
            neighbor_queue.put(n)
            node_dict[n[1]] = {
                "sum_distance": n[0],
                "preceding": curr_node,
                "queue_ref": n,
            }

        while curr_node != end_node and not neighbor_queue.empty():

            curr_distance, curr_node = neighbor_queue.get()
            node_dict[curr_node]["queue_ref"] = None

            for (n_distance, n_node) in curr_node.get_neighbors():

                updated_distance = curr_distance + n_distance

                if n_node not in node_dict.keys():

                    new_node = [updated_distance, n_node]
                    neighbor_queue.put(new_node)
                    node_dict[n_node] = {
                        "sum_distance": updated_distance,
                        "preceding": curr_node,
                        "queue_ref": new_node,
                    }

                elif node_dict[n_node]["sum_distance"] > updated_distance:

                    if node_dict[n_node]["queue_ref"] == None:
                        raise AssertionError(
                            "The fetched node is already visited but the path is not optimal!"
                        )

                    node_dict[n_node]["sum_distance"] = updated_distance
                    node_dict[n_node]["preceding"] = curr_node
                    node_dict[n_node]["queue_ref"][0] = updated_distance

        if curr_node != end_node:
            print("There is no path between the nodes!")
            return []

        else:
            sum_distance = node_dict[end_node]["sum_distance"]
            print(f"Path computed successfully! Final distance is {sum_distance}")

            path = []
            while curr_node != start_node:
                path.insert(0, curr_node.node_id)
                curr_node = node_dict[curr_node]["preceding"]

            return path, sum_distance
