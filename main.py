from time import sleep

from graph2 import Vertex, Graph
from triest_baseex import TriestBase
import networkx as nx

def create_stream(graph):
    def stream():
        for edge in graph.edges:
            yield edge
    return stream

if __name__ == '__main__':
    graph = nx.complete_graph(10)
    graph = graph.to_undirected()

    triest = TriestBase(10)
    stream = create_stream(graph)
    triest.calculate_triangles(stream)
    print(triest)
    print("networkx", nx.triangles(graph))


