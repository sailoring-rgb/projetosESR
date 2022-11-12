import socket
import threading
import re
import heapq as hq
from tabulate import tabulate


def populateGraph(vertices,neighbors):
    graph = [[0 for column in range(vertices)] for row in range(vertices)]
    for row in range(vertices): # row = 0, 1, 2 ou 3
        for column in range(vertices): # column = 0, 1, 2 ou 3
            for element in range(len(neighbors)):
                if row == neighbors[element][0] and column == neighbors[element][1]:
                    graph[row][column] = 1
                    graph[column][row] = 1
                    break
    return graph


class Graph():
 
 
    def __init__(self,vertices,nodes,neighbors):
        self.numVert = vertices
        self.nodes = nodes
        self.graph = populateGraph(vertices,neighbors)


    def minDistance(self, time, visited):
        min = 1e7
        for v in range(self.numVert):
            if time[v] < min and visited[v] == False:
                min = time[v]
                min_index = v
        return min_index
 

    def dijkstra(self, src):
        time = [1e7] * self.numVert
        time[src] = 0
        visited = [False] * self.numVert
        for cout in range(self.numVert):
            row = self.minDistance(time, visited)
            visited[row] = True
            for column in range(self.numVert):
                if (self.graph[row][column] > 0 and visited[column] == False and time[column] > time[row] + self.graph[row][column]):
                    time[column] = time[row] + self.graph[row][column]
        return time
    

    def generateFile(self):
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

        f = open("topology.csv", "w")
        f.write(tabulate(table))
        f.close()