from triest_baseex import TriestBase
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
    sizes = [5000, 10000, 20000, 30000, 90000]
    # graph = nx.complete_graph(10)
    graph2 = nx.read_edgelist("datasets/facebook_combined.txt", comments="#", create_using=DiGraph)
    graph2 = graph2.to_undirected()
    actual_num_triangles = 1612010

    results_per_size = {"memory_size": [], "average": [], "variance": [], "median": [], "true_value": [], "abs_average_diff": [],
                        "abs_median_diff": []}
    for memory_size in sizes:
        results = []
        for count in range(0, 4):
            triest = TriestBase(memory_size)
            stream = create_stream(graph2)
            triangles_global, triangles_per_node = triest.calculate_triangles(stream)
            results.append(triangles_global)

        average_estimation = np.mean(results)
        variance = np.var(results)

        median_estimation = np.median(results)
        results_per_size["memory_size"].append(memory_size)
        results_per_size["average"].append(average_estimation)
        results_per_size["abs_average_diff"].append(abs(average_estimation-actual_num_triangles))
        results_per_size["variance"].append(variance)
        results_per_size["median"].append(median_estimation)
        results_per_size["abs_median_diff"].append(abs(median_estimation - actual_num_triangles))
        results_per_size["true_value"].append(actual_num_triangles)
        print("----------------------------------------") 
        print("size: ", memory_size)
        print("average : triangles_global: ", average_estimation)
        print(f"median estimation: {median_estimation}")
        # print("networkx", sum(nx.triangles(graph2).values()) / 3) # this is the actual global number of triangles estimated by networkx
        print("Average diff :", (abs(average_estimation - actual_num_triangles)))
        print("Median diff :", (abs(median_estimation - actual_num_triangles)))

    df = pd.DataFrame(results_per_size)
    df.to_csv('results_per_size.csv', index=True)
    print("**************** average ****************")
    display(df)
