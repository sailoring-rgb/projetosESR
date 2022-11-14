import re

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

    # RECEBER COMANDO ...
    
    def constructGraph(command):
        nodes = []
        pairs = re.findall("(?:\[(.*?)\])",command) #['A:B,C', 'B:C', 'C:D,E']
        neighbors = []   # [ (indA,indB,distanceAB), (indA,indB,distanceAC), (ind,C,distanceBC) ]
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
                neighbors.append((getIndex(nodes,interf1.ip),(getIndex(nodes,interf2.ip))))

        return nodes,neighbors