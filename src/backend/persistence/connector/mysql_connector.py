import os
from typing import List, Optional

import mysql.connector
from GooglePathFinder.src.backend.persistence.connector.interface.connector import Connector
from GooglePathFinder.src.backend.persistence.connector.model.nodedao import NodeDao


class MySQLConnector(Connector):

    def _connect(self):
        self._db = mysql.connector.connect(
            host=os.getenv("PATHFINDER_HOST", "host"),
            user=os.getenv("DB_USERNAME", "admin"),
            passwd=os.getenv("PATHFINDER_PASSWORD", "password"),
            database=os.getenv("DB_DATABASE", "PATHFINDER")
        )
        if self._db.cursor:
            print("Successful connection to database.")

    def find_all(self) -> List[NodeDao]:
        self._connect()
        cursor = self._db.cursor()
        cursor.execute("""
        SELECT NODE_ID, NODE_NAME, CITY, ZIP_CODE, LONGITUDE, LATITUDE, HEURISTICS
        FROM PATHFINDER.NODES""")

        columns = tuple([d[0] for d in cursor.description])

        result = [dict(zip(columns, row)) for row in cursor]

        cursor.close()
        self._db.close()

        return [NodeDao(item) for item in result]

    def find_node_by_id(self, node_id : str) -> Optional[NodeDao]:
        self._connect()
        cursor = self._db.cursor()
        cursor.execute("""
        SELECT NODE_ID, NODE_NAME, CITY, ZIP_CODE, LONGITUDE, LATITUDE, HEURISTICS
        FROM PATHFINDER.NODES
        where NODE_ID = """ + node_id)

        columns = tuple([d[0] for d in cursor.description])

        result = [dict(zip(columns, row)) for row in cursor]
        assert len(result) <= 1

        cursor.close()
        self._db.close()

        return NodeDao(result[0]) if len(result) == 1 else None

    def find_neighbors_by_node(self, node_id: str) -> List[NodeDao]:
        self._connect()
        cursor = self._db.cursor()
        cursor.execute("""
        SELECT n.NODE_ID, n.NODE_NAME, n.CITY, n.ZIP_CODE, n.LATITUDE, n.LONGITUDE, n.HEURISTICS, e.DISTANCE
        FROM PATHFINDER.NODES n LEFT JOIN PATHFINDER.GRAPH g ON n.node_id=g.NODE_ID 
        RIGHT JOIN PATHFINDER.EDGES e ON g.EDGE_ID=E.EDGE_ID
        WHERE e.FROM_CROSSROADS_ID = = """ + node_id)

        columns = tuple([d[0] for d in cursor.description])

        result = [dict(zip(columns, row)) for row in cursor]

        cursor.close()
        self._db.close()

        return [NodeDao(item) for item in result]

    def find_backward_neighbors_by_node(self, node_id: str) -> List[NodeDao]:
        self._connect()
        cursor = self._db.cursor()
        cursor.execute("""
            SELECT n.NODE_ID, n.NODE_NAME, n.CITY, n.ZIP_CODE, n.LATITUDE, n.LONGITUDE, n.HEURISTICS, e.DISTANCE
            FROM PATHFINDER.NODES n LEFT JOIN PATHFINDER.GRAPH g ON n.node_id=g.NODE_ID 
            RIGHT JOIN PATHFINDER.EDGES e ON g.EDGE_ID=E.EDGE_ID
            WHERE e.TO_CROSSROADS_ID = 
        """ + node_id)

        columns = tuple([d[0] for d in cursor.description])

        result = [dict(zip(columns, row)) for row in cursor]

        cursor.close()
        self._db.close()

        return [NodeDao(item) for item in result]
