import csv
import os
import mysql.connector

cnx = mysql.connector.connect(
  host=os.getenv("PATHFINDER_HOST", "host"),
  user=os.getenv("DB_USERNAME", "admin"),
  passwd=os.getenv("PATHFINDER_PASSWORD", "password"),
  database=os.getenv("DB_DATABASE", "PATHFINDER")
)
cursor = cnx.cursor()

nodes = csv.DictReader(open("../resources/offline_dataset/nodes.csv"))
edges = csv.DictReader(open("../resources/offline_dataset/edges.csv"))

add_node = ("INSERT INTO PATHFINDER.NODES "
            "(NODE_ID, NODE_NAME, CITY, ZIP_CODE, LATITUDE, LONGITUDE, HEURISTICS) "
            "VALUES (%(id)s, %(name)s, %(city)s, %(zipcode)s, %(lat)s, %(lon)s, %(heuristics)s)")


for row in nodes:
  data_node = {
    "id": row['NODE_ID'],
    "name": 'dummy',
    "city": 'dummy',
    "zipcode": 0,
    "lat": row['LATITUDE'],
    "lon": row['LONGITUDE'],
    "heuristics": 0
  }
  cursor.execute(add_node, data_node)

add_edge = ("INSERT INTO PATHFINDER.EDGES "
            "(EDGE_ID, EDGE_NAME, FROM_ID, TO_ID, DISTANCE) "
            "VALUES (%(id)s, %(name)s, %(from)s, %(to)s, %(dist)s)")

counter = 0
for row in edges:
  data_edge = {
    "id": counter,
    "name": 'dummy',
    "from": row['FROM_ID'],
    "to": row['TO_ID'],
    "dist": row['DISTANCE']
  }
  cursor.execute(add_edge, data_edge)
  counter +=1

cnx.commit()

cursor.close()
cnx.close()
