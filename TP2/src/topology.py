from tabulate import tabulate
from oNode import oNode
from graph import graph

def shortestPathsToFile(self):
    table = []
    header = []
    header.append("Node")
    for node in range(self.numVert):
        header.append(f" \t Time from {self.nodes[node].ip}")
    table.append(header)
    for node in range(self.numVert):
        values = []
        values.append(self.nodes[node].ip)
        values = values + self.dijkstra(node)
        table.append(values)

    f = open("shortestPaths.csv", "w")
    f.write(tabulate(table))
    f.close()


# COMMAND EXAMPLE:
# 'oNode [10.0.0.1 : 10.0.0.2 , 10.0.0.3] [10.0.0.2 : 10.0.0.3, 10.0.0.6]'
# index:     0           1          2          1          2         3
app = oNode()
nodes,neighbors = app.constructGraph('oNode [10.0.0.1 : 10.0.0.2 , 10.0.0.3] [10.0.0.2 : 10.0.0.3, 10.0.0.6]')

graph = graph(len(nodes),nodes,neighbors)
shortestPathsToFile()