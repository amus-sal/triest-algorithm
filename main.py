from triest_baseex_imp import TriestBase
import networkx as nx
from networkx import DiGraph

def create_stream(graph):
    def stream():
        for edge in graph.edges:
            yield edge
    return stream


if __name__ == '__main__':
    num_nodes = 1000
    graph = nx.complete_graph(10)
    graph2 = nx.read_edgelist("datasets/facebook_combined.txt", comments="#", create_using=DiGraph)
    graph2 = graph2.to_undirected()
    num_edges = len(graph.edges)
    print("full graph num edges", len(graph.edges))
    triest = TriestBase(num_nodes * 3) # num_nodes * 3 seems very effective for the clique graph
    stream = create_stream(graph2)
    triangles_global, triangles_per_node = triest.calculate_triangles(stream)

    print("triangles_global: ", triangles_global)
    print("networkx", sum(nx.triangles(graph2).values()) / 3) # this is the actual global number of triangles estimated by networkx


