import socket
import threading
import re
import heapq as hq
import math

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
 
    def __init__(self,vertices,neighbors):
        self.V = vertices
        self.graph = populateGraph(vertices,neighbors)

    def printSolution(self, dist):
        print("Vertex \t Distance from Source")
        for node in range(self.V):
            print(node, "\t\t", dist[node])


    # A utility function to find the vertex with
    # minimum distance value, from the set of vertices
    # not yet included in shortest path tree
    def minDistance(self, time, sptSet):
 
        # Initialize minimum distance for next node
        min = 1e7
 
        # Search not nearest vertex not in the
        # shortest path tree
        for v in range(self.V):
            if time[v] < min and sptSet[v] == False:
                min = time[v]
                min_index = v
 
        return min_index
 
    # Function that implements Dijkstra's single source
    # shortest path algorithm for a graph represented
    # using adjacency matrix representation
    def dijkstra(self, src):
 
        time = [1e7] * self.V
        time[src] = 0
        # sptSet (shortest path tree set) keeps track of vertices included in shortest path tree, i.e., 
        # whose minimum distance from source is calculated and finalized.
        sptSet = [False] * self.V
 
        for cout in range(self.V):
 
            # Pick the minimum distance vertex from
            # the set of vertices not yet processed.
            # u is always equal to src in first iteration
            #print("-------------------")
            #print(time)
            #print(sptSet)
            u = self.minDistance(time, sptSet)
            #print(u)
 
            # Put the minimum distance vertex in the
            # shortest path tree
            sptSet[u] = True
 
            # Update dist value of the adjacent vertices
            # of the picked vertex only if the current
            # distance is greater than new distance and
            # the vertex in not in the shortest path tree
            for column in range(self.V):
                if (self.graph[u][column] > 0 and sptSet[column] == False and time[column] > time[u] + self.graph[u][column]):
                    time[column] = time[u] + self.graph[u][column]

        self.printSolution(time)