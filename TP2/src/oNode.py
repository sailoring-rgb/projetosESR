import socket
import threading
import re

class interface:

    def __init__(self, nodeName, ip):
        self.nodeName = nodeName
        self.ip = ip

class oNode:

    # oNode [ip1:ip2] [ip2:ip3] [ip3:ip4,ip5]
    def constructGraph(command):
        graph = {}
        pairs = re.findall("(?:\[(.*?)\])",command) #['A:B', 'B:C', 'C:D,E']
        for p in pairs:
            ips = p.split(' : ') # 'A', 'B'
            ips2 = ips[1].split(',')
            graph[f'{ips[0]}'] = ips2
        return graph

