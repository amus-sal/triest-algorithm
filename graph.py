from time import sleep

class Graph:
    def __init__(self):
        self.adjacency_list = {}
        self.edges = []

    def neighbor_edges(self, node):
        neighbors = self.adjacency_list[node]
        return [(node, n) for n in neighbors]

    def neighbors(self, node):
        return self.adjacency_list[node]

    def add_edge(self, edge):
        (u, v) = edge
        self.edges.append((u, v))
        try:
            self.adjacency_list[u].append(v)
        except:
            self.adjacency_list[u] = [v]
        try:
            self.adjacency_list[v].append(u)
        except:
            self.adjacency_list[v] = [u]


    def remove_edge(self, u, v):
        self.adjacency_list[u].remove(v)
        self.adjacency_list[v].remove(u)
        self.edges.remove((u, v))

    def get_edge_as_stream(self):
        for edge in self.graph.edges:
            # sleep(1)
            yield edge
