import re
import threading
from time import sleep, perf_counter


# ----------------------- GRAFO -----------------------
class graph:
    def __init__(self, vertices, nodes, neighbors):
        self.numVert = vertices  # número de vértices do grafo
        self.nodes = nodes  # nodos da rede overlay
        self.graph = self.populateGraphInit(vertices, neighbors)

    def populateGraphInit(self, vertices, neighbors):
        graph = [[0 for column in range(vertices)] for row in range(vertices)]
        for row in range(vertices):  # row = 0, 1, 2 ou 3
            for column in range(vertices):  # column = 0, 1, 2 ou 3
                for element in range(len(neighbors)):
                    if row == neighbors[element][0] and column == neighbors[element][1]:
                        graph[row][column] = 1
                        graph[column][row] = 1
                        break
        return graph

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
        for count in range(self.numVert):
            row = self.minDistance(time, visited)
            visited[row] = True
            for column in range(self.numVert):
                if (self.graph[row][column] > 0 and visited[column] == False and time[column] > time[row] +
                        self.graph[row][column]):
                    time[column] = time[row] + self.graph[row][column]
        return time


# ------------------ INTERFACE (NODO) ------------------
class interface:

    def __init__(self, ip, requiredFiles, currentFiles):
        self.ip = ip  # ips das interfaces ligadas aos nodos
        self.requiredFiles = requiredFiles  # lista de ficheiros que ele quer
        self.currentFiles = currentFiles  # lista de ficheiros que ele tem


# ----------------------- oNode -----------------------

command = '[10.0.0.1 : 10.0.0.2 , 10.0.0.3] [10.0.0.2 : 10.0.0.3, 10.0.0.6]'
my_id = 'oNode1'


def overlayNetwork(command):
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


def clientHandler():
    print('a iniciar client...')
    while (True):
        print('*doing client stuff*')
        sleep(2)


def mensagem(true_sender_id, sender_id, n_saltos, timestamps, tree_back_to_sender):
    # timestamps - dicionario de (nodo: tempo) das mensagens recebidas
    timestamps[my_id] = datetime.now()

    # tree_back_to_sender - grafo de caminhos mais curtos

    # adicionar my_id

    return true_sender_id, my_id, n_saltos + 1, timestamps, tree_back_to_sender


def serverHandler():
    print('a iniciar servidor servidor...')
    while (True):
        sleep(1)


start_time = perf_counter()

# task goes here

end_time = perf_counter()
print(f'It took {end_time - start_time: 0.2f} second(s) to complete.')
threads = []

cliente = threading.Thread(target=clientHandler, args=())
cliente.start()

servidor = threading.Thread(target=serverHandler, args=())
servidor.start()

servidor.join()
cliente.join()
