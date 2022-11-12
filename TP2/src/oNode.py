import socket
import threading
import re
from dijkstra import Graph


class interface:

    def __init__(self, ip, requiredFiles,currentFiles):
        self.ip = ip                           # ips das interfaces ligadas aos nodos 
        self.requiredFiles = requiredFiles     # lista de ficheiros que ele quer
        self.currentFiles = currentFiles       # lista de ficheiros que ele tem


def getIndex(li,ip):
    for index, x in enumerate(li):
        if x.ip == ip:
            return index
    return -1


class oNode:

    # oNode [ip1:ip2] [ip2:ip3,ip4] [ip3:ip4,ip5]
    def constructGraph(command):
        nodes = []
        pairs = re.findall("(?:\[(.*?)\])",command) #['A:B,C', 'B:C', 'C:D,E']
        neighbors_aux = []   # [ (indA,indB,distanceAB), (indA,indB,distanceAC), (ind,C,distanceBC) ]
        for p in pairs:
            ips = re.split(r'\s*:\s*', p) # 'C', 'D,E'
            interf1 = interface(ips[0],[],[])
            if not any(obj.ip == ips[0] for obj in nodes):
                nodes.append(interf1)
            ips2 = re.split(r'\s*,\s', ips[1]) # 'D', 'E'
            for next in ips2:
                interf2 = interface(next,[],[])
                if not any(obj.ip == next for obj in nodes):
                    nodes.append(interf2)
                neighbors_aux.append((interf1,interf2))

        neighbors = []
        for n in neighbors_aux:
            neighbors.append((getIndex(nodes,n[0].ip),getIndex(nodes,n[1].ip),1))

        graph = Graph(len(nodes),neighbors)

        for src in range(len(graph.graph)):
            print(graph.dijkstra(src))

        return nodes,graph

#                                     0          1          2           1         2           3
    grapf = constructGraph('oNode [10.0.0.1 : 10.0.0.2 , 10.0.0.3] [10.0.0.2 : 10.0.0.3, 10.0.0.6]')
    