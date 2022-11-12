import socket
import threading
import re
from .dijkstra import Graph

class interface:

    def __init__(self, ip, nodeName, requiredFiles,currentFiles):
        self.nodeName = nodeName               # o nome do nodos
        self.ip = ip                           # ips das interfaces ligadas aos nodos 
        self.requiredFiles = requiredFiles     # lista de ficheiros que ele quer
        self.currentFiles = currentFiles       # lista de ficheiros que ele tem

class oNode:

    # oNode [ip1:ip2] [ip2:ip3] [ip3:ip4,ip5]
    def constructGraph(command):
        graph = Graph()
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

    # grapf = constructGraph('oNode [10.0.0.1 : 10.0.0.2 , 10.0.0.3] [10.0.0.2 : 10.0.0.3, 10.0.0.6]')
