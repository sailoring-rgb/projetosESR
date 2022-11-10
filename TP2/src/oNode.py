import socket
import threading
import re

class interface:

    def __init__(self, ip, nodeName, requiredFiles,currentFiles):
        self.nodeName = nodeName
        self.ip = ip
        self.requiredFiles = requiredFiles     # lista de ficheiros que ele quer
        self.currentFiles = currentFiles       # lista de ficheiros que ele tem

class oNode:

    # oNode [ip1:ip2] [ip2:ip3] [ip3:ip4,ip5]
    def constructGraph(command):
        graph = {}
        pairs = re.findall("(?:\[(.*?)\])",command) #['A:B', 'B:C', 'C:D,E']
        i = 0
        for p in pairs:
            ips = re.split(r'\s*:\s*', p) # 'C', 'D,E'
            interf1 = interface(ips[0],f'node{i}',[],[])
            ips2 = re.split(r'\s*,\s', ips[1]) # 'D', 'E'
            neighbors = []
            for next in ips2:
                interf2 = interface(next,f'node{i}',[],[])
                neighbors.append(interf2)
                i = i+1
            graph[interf1] = neighbors
        return graph

    grapf = constructGraph('oNode [10.0.0.1 : 10.0.0.2 , 10.0.0.3] [10.0.0.2 : 10.0.0.3, 10.0.0.6]')

"""
def dijkstra(graph, start_vertex):
    D = {v:float('inf') for v in range(graph.v)}
    D[start_vertex] = 0

    pq = PriorityQueue()
    pq.put((0, start_vertex))

    while not pq.empty():
        (dist, current_vertex) = pq.get()
        graph.visited.append(current_vertex)

        for neighbor in range(graph.v):
            if graph.edges[current_vertex][neighbor] != -1:
                distance = graph.edges[current_vertex][neighbor]
                if neighbor not in graph.visited:
                    old_cost = D[neighbor]
                    new_cost = D[current_vertex] + distance
                    if new_cost < old_cost:
                        pq.put((new_cost, neighbor))
                        D[neighbor] = new_cost
    return D
"""