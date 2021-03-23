from typing import List

from src.persistence.model.city import City


class Connector:
    def __init__(self):
        pass

    def find_all(self) -> List[City]:
        pass

    def find_neighbors_by_city(self, city: str) -> List[City]:
        pass
