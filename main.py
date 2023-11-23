from time import sleep

from graph2 import Vertex, Graph
from triest_base import TriestBase
import networkx as nx

def create_stream():
    graph = nx.complete_graph(10)
    graph = graph.to_undirected()
    for edge in graph.edges:
        sleep(0.5)
        yield edge

if __name__ == '__main__':

    a = Vertex('A')
    b = Vertex('B')
    c = Vertex('C')
    d = Vertex('D')
    e = Vertex('E')

    a.add_neighbors([b, c, e])
    b.add_neighbors([a, c])
    c.add_neighbors([b, d, a, e])
    d.add_neighbor(c)
    e.add_neighbors([a, c])

    g = Graph()
    g.add_vertices([a, b, c, d, e])
    g.add_edge(b, d)

    triest = TriestBase(10)
    stream = create_stream()
    triest.calculate_triangles(stream)
    print(triest)
    # print(nx.triangles(g.graph))


