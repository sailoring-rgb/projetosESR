def breadth_first_search(graph, start):
    # create a queue for tracking
    queue = []

    # create a set for storing visited nodes
    visited = set()

    # enqueue the starting node
    queue.append(start)
    visited.add(start)

    # while there are nodes in the queue
    while queue:
        # dequeue the first node in the queue
        current = queue.pop(0)
        print(current)

        # get the neighbors of the current node
        neighbors = graph[current]

        # for each neighbor of the current node
        for neighbor in neighbors:
            # if the neighbor has not been visited
            if neighbor not in visited:
                # enqueue the neighbor
                queue.append(neighbor)
                visited.add(neighbor)


# test the breadth-first search function
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

breadth_first_search(graph, 'A')
