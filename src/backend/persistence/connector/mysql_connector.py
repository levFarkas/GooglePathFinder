import mysql.connector

from backend.persistence.connector.interface.connector import Connector


class MySQLConnector(Connector):
    def __init__(self):
        super().__init__()
        self._db = mysql.connector.connect(
            host="localhost",
            user="your_username_here",
            passwd="your_mysql_password_here",
            database="your_database_name_here"
        )
        if self._db.cursor:
            print("Successful connection to database.")
