import os
from typing import List

import mysql.connector

from GooglePathFinder.src.backend.persistence.connector.interface.connector import Connector
from GooglePathFinder.src.backend.persistence.connector.model.nodedao import NodeDao


class MySQLConnector(Connector):
    def __init__(self):
        super().__init__()
        self._db = mysql.connector.connect(
            host=os.getenv("DB_HOST", "host"),
            user=os.getenv("DB_USERNAME", "admin"),
            passwd=os.getenv("DB_PASSWORD", "password"),
            database=os.getenv("DB_DATABASE", "PATHFINDER")
        )
        if self._db.cursor:
            print("Successful connection to database.")

    def find_all(self) -> List[NodeDao]:
        cursor = self._db.cursor()
        cursor.execute("""
        SELECT NODE_ID, NODE_NAME, CITY, ZIP_CODE, LONGITUDE, LATITUDE, HEURISTICS 
        FROM PATHFINDER.NODES""")

        columns = tuple([d[0] for d in cursor.description])

        result = [dict(zip(columns, row)) for row in cursor]

        cursor.close()

        return [NodeDao(item) for item in result]

    def find_neighbors_by_node(self, node_id: str) -> List[NodeDao]:
        cursor = self._db.cursor()
        cursor.execute("""
        SELECT n2.NODE_ID, n2.NODE_NAME, n2.CITY, n2.ZIP_CODE, n2.LONGITUDE, n2.LATITUDE, n2.HEURISTICS 
        FROM PATHFINDER.EDGES e
        INNER JOIN PATHFINDER.NODES n on n.NODE_ID = e.FROM_CROSSROADS_ID 
        INNER JOIN PATHFINDER.NODES n2 on n2.NODE_ID = e.TO_CROSSROADS_ID 
        where n.NODE_ID = """ + node_id)

        columns = tuple([d[0] for d in cursor.description])

        result = [dict(zip(columns, row)) for row in cursor]

        cursor.close()

        return [NodeDao(item) for item in result]

    def find_backward_neighbors_by_node(self, node_id: str) -> List[NodeDao]:
        cursor = self._db.cursor()
        cursor.execute("""
        SELECT n2.NODE_ID, n2.NODE_NAME, n2.CITY, n2.ZIP_CODE, n2.LONGITUDE, n2.LATITUDE, n2.HEURISTICS 
        FROM PATHFINDER.EDGES e
        INNER JOIN PATHFINDER.NODES n on n.NODE_ID = e.TO_CROSSROADS_ID 
        INNER JOIN PATHFINDER.NODES n2 on n2.NODE_ID = e.FROM_CROSSROADS_ID 
        where n.NODE_ID = """ + node_id)

        columns = tuple([d[0] for d in cursor.description])

        result = [dict(zip(columns, row)) for row in cursor]

        cursor.close()

        return [NodeDao(item) for item in result]
