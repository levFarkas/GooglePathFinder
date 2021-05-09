from GooglePathFinder.src.model.node import Node


class NodeDao:
    def __init__(self, data: dict):
        self.node_id = data["NODE_ID"]
        self.latitude = float(data["LATITUDE"])
        self.longitude = float(data["LONGITUDE"])
        self.city = ""
        self.heuristic = 0

        if "NODE_NAME" in data.keys():
            self.node_name = data["NODE_NAME"]
        if "CITY" in data.keys():
            self.city = data["CITY"]
        if "ZIP_CODE" in data.keys():
            self.zip = data["ZIP_CODE"]
        if "HEURISTICS" in data.keys():
            self.heuristic = float(data["HEURISTICS"])
        if "DISTANCE" in data.keys():
            self.distance = float(data["DISTANCE"])

    def convert_to_node_model(self) -> Node:
        return Node(
            node_id=self.node_id,
            longitude=self.longitude,
            latitude=self.latitude,
            heuristics=self.heuristic,
            city=self.city)
