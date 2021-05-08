from src.model.node import Node


class NodeDao:
    def __init__(self, data: dict):
        self.node_id = data["NODE_ID"]
        self.node_name = data["NODE_NAME"]
        self.city = data["CITY"]
        self.zip = data["ZIP_CODE"]
        self.latitude = data["LATITUDE"]
        self.longitude = data["LONGITUDE"]
        self.heuristic = data["HEURISTICS"]
        self.distance = data["DISTANCE"]

    def convert_to_node_model(self) -> Node:
        return Node(
            node_id=self.node_id,
            longitude=self.longitude,
            latitude=self.latitude,
            heuristics=self.heuristic,
            city=self.city)
