import os
from typing import List, Optional
import logging
import atexit

import mysql.connector
from GooglePathFinder.src.backend.persistence.connector.interface.connector import Connector
from GooglePathFinder.src.backend.persistence.connector.model.nodedao import NodeDao


class MySQLConnector(Connector):
    def __init__(self):
        self._connect()
        atexit.register(self._disconnect)

    def _connect(self):
        self._db = mysql.connector.connect(
            host=os.getenv("PATHFINDER_HOST", "host"),
            user=os.getenv("DB_USERNAME", "admin"),
            passwd=os.getenv("PATHFINDER_PASSWORD", "password"),
            database=os.getenv("DB_DATABASE", "PATHFINDER")
        )
        if self._db.cursor:
            logging.info("Successful connection to the database.")
        else:
            logging.warning("Couldn't connect to the database.")
    
    def _disconnect(self):
        self._db.close()

    def find_all(self) -> List[NodeDao]:
        cursor = self._db.cursor()
        try:
            cursor.execute("""
                SELECT * FROM PATHFINDER.NODES""")
            columns = tuple([d[0] for d in cursor.description])
            result = [dict(zip(columns, row)) for row in cursor]
            cursor.close()
            return [NodeDao(item) for item in result]
        except Exception as e:
            logging.warning("Error when querying all nodes.")
            logging.warning(e)

        return []

    def find_node_by_id(self, node_id : str) -> Optional[NodeDao]:
        try:
            cursor = self._db.cursor()
            cursor.execute("""
                SELECT NODE_ID , NODE_NAME , CITY , ZIP_CODE , LATITUDE , LONGITUDE , HEURISTICS
                FROM PATHFINDER.NODES
                where NODE_ID = """ + str(node_id))
            columns = tuple([d[0] for d in cursor.description])
            result = [dict(zip(columns, row)) for row in cursor]
            assert len(result) <= 1
            cursor.close()
            return NodeDao(result[0]) if len(result) == 1 else None
        except Exception as e:
            logging.warning("Error when querying node by id.")
            logging.warning(e)

        return None

    def find_neighbors_by_node(self, node_id: str) -> List[NodeDao]:
        try:
            cursor = self._db.cursor()
            cursor.execute("""
                SELECT e.DISTANCE , n2.NODE_ID , n2.LATITUDE , n2.LONGITUDE 
                FROM PATHFINDER.NODES n1 INNER JOIN EDGES e ON n1.NODE_ID = e.FROM_ID 
                INNER JOIN PATHFINDER.NODES n2 ON e.TO_ID = n2.NODE_ID 
                WHERE e.FROM_ID =""" + str(node_id))
            columns = tuple([d[0] for d in cursor.description])
            result = [dict(zip(columns, row)) for row in cursor]
            cursor.close()
            logging.info(result)
            return [NodeDao(item) for item in result]
        except Exception as e:
            logging.warning("Error when querying neighbors.")
            logging.warning(e)
        
        return []

    def find_backward_neighbors_by_node(self, node_id: str) -> List[NodeDao]:
        try:
            cursor = self._db.cursor()
            cursor.execute("""
                SELECT e.DISTANCE , n2.NODE_ID, n2.LATITUDE , n2.LONGITUDE 
                FROM PATHFINDER.NODES n1 INNER JOIN EDGES e ON n1.NODE_ID = e.FROM_ID 
                INNER JOIN PATHFINDER.NODES n2 ON e.FROM_ID = n2.NODE_ID 
                WHERE e.TO_ID =""" + str(node_id))
            columns = tuple([d[0] for d in cursor.description])
            result = [dict(zip(columns, row)) for row in cursor]
            cursor.close()
            return [NodeDao(item) for item in result]
        except Exception as e:
            logging.warning("Error when querying backward neighbors.")
            logging.warning(e)

        return []
