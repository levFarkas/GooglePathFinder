class Node:
    def __init__(self, data: dict):
        self.node_id = data["NODE_ID"]
        self.node_name = data["NODE_ID"]
        self.city = data["CITY"]
        self.zip = data["ZIP_CODE"]
        self.latitude = data["LATITUDE"]
        self.longitude = data["LONGITUDE"]
        self.heuristic = data["HEURISTICS"]
