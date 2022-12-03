from collections import deque

class Graph:
  def __init__(self):
    self.nodes = set()
    self.edges = dict()

  def add_node(self, node):
    self.nodes.add(node)

  def add_edge(self, node1, node2):
    if node1 not in self.edges:
      self.edges[node1] = set()
    self.edges[node1].add(node2)

  def flood(self, source, message):
    visited = set()
    queue = deque([source])

    while queue:
      current = queue.popleft()
      visited.add(current)

      print('Sending message to %s: %s' % (current, message))

      if current in self.edges:
        for neighbor in self.edges[current]:
          if neighbor not in visited:
            queue.append(neighbor)

# create a new graph
g = Graph()

# add some nodes to the graph
g.add_node('A')
g.add_node('B')
g.add_node('C')
g.add_node('D')
g.add_node('E')
g.add_node('F')

# add some edges to the graph
g.add_edge('A', 'B')
g.add_edge('A', 'C')
g.add_edge('B', 'D')
g.add_edge('B', 'E')
g.add_edge('C', 'F')
g.add_edge('E', 'F')

# flood the graph with a message
g.flood('A', 'Hello, World!')