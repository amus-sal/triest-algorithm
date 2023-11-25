from triest_baseex import TriestBase
import networkx as nx

def create_stream(graph):
    def stream():
        for edge in graph.edges:
            yield edge
    return stream

if __name__ == '__main__':
    num_nodes = 10
    graph = nx.complete_graph(10)
    graph = graph.to_undirected()
    num_edges = len(graph.edges)
    print("full graph num edges", len(graph.edges))
    triest = TriestBase(num_nodes * 3)
    stream = create_stream(graph)
    triangles_global, triangles_per_node = triest.calculate_triangles(stream)

    print("triangles_global: ", triangles_global)
    print("networkx", sum(nx.triangles(graph).values()) / 3)


