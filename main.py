from triest_baseex_imp import TriestBase
import networkx as nx
from networkx import DiGraph
import numpy as np
import pandas as pd
from IPython.display import display

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
    actual_num_triangles = 1612010

    results_per_size_average = {}
    results_per_size_median = {}
    for size in sizes:
        results = []
        for count in range(0, 4):
            triest = TriestBase(size)
            stream = create_stream(graph2)
            triangles_global, triangles_per_node = triest.calculate_triangles(stream)
            results.append(triangles_global)

        average_estimation = np.mean(results)
        median_estimation = np.median(results)
        results_per_size_average[size] = average_estimation
        results_per_size_median[size] = median_estimation

        print("----------------------------------------") 
        print("size: ", size)
        print("average : triangles_global: ", average_estimation)
        print(f"median estimation: {median_estimation}")
        # print("networkx", sum(nx.triangles(graph2).values()) / 3) # this is the actual global number of triangles estimated by networkx
        print("Median diff :", (abs(average_estimation - actual_num_triangles)))
        print("Median diff :", (abs(median_estimation - actual_num_triangles)))
 

        average_df = pd.Dataframe(results_per_size_average)
        median_df = pd.Dataframe(results_per_size_median)

        print("**************** average ****************")
        display(average_df)
        print("**************** median ****************")
        display(median_df)