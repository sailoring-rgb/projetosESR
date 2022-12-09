import re
from threading import Thread
import time


# import server
# import client

def getIndex(li, ip):
    for index, x in enumerate(li):
        if x.ip == ip:
            return index
    return -1


# ------------------ INTERFACE (NODO) ------------------
class interface:

    def __init__(self, ip, requiredFiles, currentFiles):
        self.ip = ip  # ips das interfaces ligadas aos nodos
        self.requiredFiles = requiredFiles  # lista de ficheiros que ele quer
        self.currentFiles = currentFiles  # lista de ficheiros que ele tem


"""
# ---------------------- THREADS ----------------------
class threads:

    def thread1(self):
        server()

    def thread2(self):
        client()
    
    def thread3(self):
        pass
"""


# --------------------- APP ONODE ---------------------
class oNode:

    def __init__(self):
        pass

    def overlayNetwork(self, command):
        nodes = []
        pairs = re.findall("(?:\[(.*?)\])", command)  # ['A:B,C', 'B:C', 'C:D,E']
        neighbors = []  # [ (indA,indB,distanceAB), (indA,indB,distanceAC), (ind,C,distanceBC) ]
        for p in pairs:
            ips = re.split(r'\s*:\s*', p)  # 'C', 'D,E'
            interf1 = interface(ips[0], [], [])
            if not any(obj.ip == ips[0] for obj in nodes):
                nodes.append(interf1)
            ips2 = re.split(r'\s*,\s', ips[1])  # 'D', 'E'
            for next in ips2:
                interf2 = interface(next, [], [])
                if not any(obj.ip == next for obj in nodes):
                    nodes.append(interf2)
                neighbors.append((getIndex(nodes, interf1.ip), (getIndex(nodes, interf2.ip))))
        return nodes, neighbors

    """
    def start():
        server = Thread(target=threads().thread1(), args=())
        client = Thread(target=threads().thread2(), args=())
        updateRouteTable = Thread(target=threads().thread3(), args=())
        # server.start()
        # client.start()
        # updateRouteTable.start()
        # server.join()
        # client.join()
        # updateRouteTable.join()
    """
