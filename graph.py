from time import sleep

class Graph:
    def __init__(self):
        self.adjacency_list

    def neighbor_edges(self, node):
        neighbors = self.graph.neighbors(node)
        return [(node, n) for n in neighbors]

    def add_edge(self, u, v):
        self.graph.add_edge(u, v)

    def add_node(self, u):
        self.graph.add_node(u)

    def visualize(self):
        pass

    def get_edge_as_stream(self):
        for edge in self.graph.edges:
            sleep(1)
            yield edge
