from tabulate import tabulate
from src.old.oNode import oNode
from src.old.graph import graph


def routeTableInFile(graph):
    table = []
    header = ["Node"]
    for node in range(graph.numVert):
        header.append(f" \t Time from {nodes[node].ip}")
    table.append(header)
    for node in range(graph.numVert):
        values = [nodes[node].ip]
        values = values + graph.dijkstra(node)
        table.append(values)

    f = open("routeTable.csv", "w")
    f.write(tabulate(table))
    f.close()

    # COMMAND EXAMPLE:
    # 'oNode [10.0.0.1 : 10.0.0.2 , 10.0.0.3] [10.0.0.2 : 10.0.0.3, 10.0.0.6]'
    # index:     0           1          2          1          2         3


app = oNode()
nodes, neighbors = app.overlayNetwork('oNode [10.0.0.1 : 10.0.0.2 , 10.0.0.3] [10.0.0.2 : 10.0.0.3, 10.0.0.6]')

graph = graph(len(nodes), nodes, neighbors)
routeTableInFile(graph)
