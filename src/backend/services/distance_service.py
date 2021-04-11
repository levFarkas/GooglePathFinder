from backend.persistence.connector.csv_connector import CSVConnector


class DistanceService:

    def __init__(self):
        self._connector = CSVConnector()

    def get_all_nodes(self):
        self._connector.find_all()

    def get_neighbours_by_node(self, node: str):
        self._connector.find_neighbors_by_node(node)
