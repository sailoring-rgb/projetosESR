import socket
import threading
import re
import oNode
import heapq as hq
import math

oNode = oNode()

# command = sys.argv[1:]
graph = oNode.constructGraph('oNode [10.0.0.1 : 10.0.0.2 , 10.0.0.3] [10.0.0.2 : 10.0.0.3, 10.0.0.6] [10.0.0.3 :] [10.0.0.6 :]')
# graph = {'10.0.0.1' : ['10.0.0.2' , '10.0.0.3'], '10.0.0.2' : ['10.0.0.3', '10.0.0.6'], '10.0.0.3 :[]', '10.0.0.6 :'[]}


# Python program for Dijkstra's single
# source shortest path algorithm. The program is
# for adjacency matrix representation of the graph
class Graph():
 
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)]
                      for row in range(vertices)]
        
 
    def printSolution(self, dist):
        print("Vertex \t Distance from Source")
        for node in range(self.V):
            print(node, "\t\t", dist[node])


# Function that implements Dijkstra's single source
# shortest path algorithm for a graph represented
# using adjacency matrix representation
def dijkstra(self, src):

    dist = [1e7] * self.V
    dist[src] = 0
    sptSet = [False] * self.V

    for cout in range(self.V):

        # Pick the minimum distance vertex from
        # the set of vertices not yet processed.
        # u is always equal to src in first iteration
        u = self.minDistance(dist, sptSet)

        # Put the minimum distance vertex in the
        # shortest path tree
        sptSet[u] = True

        # Update dist value of the adjacent vertices
        # of the picked vertex only if the current
        # distance is greater than new distance and
        # the vertex in not in the shortest path tree
        for v in range(self.V):
            if (self.graph[u][v] > 0 and
                sptSet[v] == False and
                dist[v] > dist[u] + self.graph[u][v]):
                dist[v] = dist[u] + self.graph[u][v]

    self.printSolution(dist)
 
