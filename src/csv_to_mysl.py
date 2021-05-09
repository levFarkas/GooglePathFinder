import pandas as pd
import os
import mysql.connector

cnx = mysql.connector.connect(
  host=os.getenv("PATHFINDER_HOST", "host"),
  user=os.getenv("DB_USERNAME", "admin"),
  passwd=os.getenv("PATHFINDER_PASSWORD", "password"),
  database=os.getenv("DB_DATABASE", "PATHFINDER")
)
cursor = cnx.cursor()

nodes = pd.read("../resources/offline_dataset/nodes.csv", skiprows = 1)
edges = pd.read("../resources/offline_dataset/edges.csv", skiprows = 1)

add_node = ("INSERT INTO PATHFINDER.NODES "
            "(NODE_ID, NODE_NAME, CITY, LATITUDE, LONGITUDE) "
            "VALUES (%(id)s, %(name)s, %(city)s, %(zipcode)s, %(lat)s, %(lon)s)")

for idx, row in nodes.iterrows():
  data_node = {
    "id": row['NODE_ID'],
    "name": 'dummy',
    "city": 'dummy',
    "zipcode": 'dummy',
    "lat": row['LATITUDE'],
    "lon": row['LONGITUDE']
  }
  cursor.execute(add_node, data_node)

add_edge = ("INSERT INTO PATHFINDER.EDGES "
            "(EDGE_ID, EDGE_NAME, FROM_CROSSROADS_ID, TO_CROSSROADS_ID, DISTANCE) "
            "VALUES (%(id)s, %(name)s, %(from)s, %(to)s, %(dist)s)")

for idx, row in edges.iterrows():
  data_edge = {
    "id": idx,
    "name": 'dummy',
    "from": row['FROM_ID'],
    "to": row['TO_ID'],
    "dist": row['DISTANCE']
  }
  cursor.execute(add_edge, data_edge)

cnx.commit()

cursor.close()
cnx.close()
