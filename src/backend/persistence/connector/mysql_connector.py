import os

import mysql.connector

from GooglePathFinder.src.backend.persistence.connector.interface.connector import Connector


class MySQLConnector(Connector):
    def __init__(self):
        super().__init__()
        self._db = mysql.connector.connect(
            host=os.getenv("HOST", "localhost"),
            user=os.getenv("USERNAME", "admin"),
            passwd=os.getenv("PASSWORD", "admin"),
            database=os.getenv("DATABASE", "database-1")
        )
        if self._db.cursor:
            print("Successful connection to database.")
