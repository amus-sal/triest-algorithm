from triest_baseex_imp import TriestBase
import networkx as nx
from networkx import DiGraph

def create_stream(graph):
    def stream():
        for edge in graph.edges:
            yield edge
    return stream


if __name__ == '__main__':
    sizes = [1000,5000,6000,8000,10000]
    # graph = nx.complete_graph(10)
    graph2 = nx.read_edgelist("datasets/facebook_combined.txt", comments="#", create_using=DiGraph)
    graph2 = graph2.to_undirected()
    #num_edges = len(graph.edges)
    #print("full graph num edges", len(graph.edges))
    for size in sizes:
        t_avg = 0
        i = 0
        for count in range(0,4):
            i += 1
            triest = TriestBase(size)
            stream = create_stream(graph2)
            triangles_global, triangles_per_node = triest.calculate_triangles(stream)
            t_avg  += triangles_global 
            print("count: ", count)
        t_avg = t_avg/i
        print("----------------------------------------") 
        print("size: ",size) 
        print("average : triangles_global: ",t_avg)
        print("networkx", sum(nx.triangles(graph2).values()) / 3) # this is the actual global number of triangles estimated by networkx
        print("The difference is :", (abs(t_avg - 1612010)))
 

