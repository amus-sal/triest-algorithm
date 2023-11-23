import random

import numpy as np

from graph import Graph


class TriestBase:

    def __str__(self):
        return f'Global_triangles_counter: {self.global_triangles_counter} \n Local triangles: {self.local_triangle_counters}'
    def __init__(self, memory_size):
        assert memory_size >= 6
        self.sample_size = memory_size
        self.timestamp = 0
        self.global_triangles_counter = 0
        self.sample_edges = set()
        self.local_triangle_counters = {}
        self.graph = Graph()

    def calculate_triangles(self, stream):
        for edge in stream():
            print("edge ", edge)
            self.graph.add_node(edge[0])
            self.graph.add_node(edge[1])
            self.graph.add_edge(edge[0], edge[1])
            self.graph.add_edge(edge[1], edge[0])
            self.timestamp += 1
            if self.sample_edge(edge, self.timestamp):
                self.sample_edges.add(edge)
                self.update_counters("add", edge)
            print("self.sample_edges", self.sample_edges)
            print(f"local counter: {self.local_triangle_counters}")
    def sample_edge(self, edge, timestamp):
        current_prob = self.sample_size / timestamp
        if timestamp <= self.sample_size:
            return True
        elif random.random() <= current_prob:
            edge_to_remove = random.choice(tuple(self.sample_edges))
            self.sample_edges.remove(edge_to_remove)
            self.update_counters("subtract", edge_to_remove)
            return True
        else:
            return False

    def get_neighbors_in_sample(self, node):
        neighbors_in_sample = {n for n in self.graph.neighbor_edges(node) if n in self.sample_edges}
        print("neighbors_in_sample",neighbors_in_sample)
        return neighbors_in_sample

    def update_counters(self, operation, edge):
        (u, v) = edge
        u_neighbors = self.get_neighbors_in_sample(u)
        v_neighbors = self.get_neighbors_in_sample(v)
        common_neighbors = u_neighbors.intersection(v_neighbors)
        print(f"u_neighbors: {u_neighbors}")
        print(f"v_neighbors: {v_neighbors}")
        print(f"common_neighbors: {common_neighbors}")
        for c in common_neighbors:
            if operation == "subtract":
                self.global_triangles_counter -= 1
                self.local_triangle_counters[c] -= 1
                self.local_triangle_counters[u] -= 1
                self.local_triangle_counters[v] -= 1
            elif operation == "add":
                self.global_triangles_counter += 1
                self.local_triangle_counters[c] += 1
                self.local_triangle_counters[u] += 1
                self.local_triangle_counters[v] += 1
        return None


s = {1, 2, 3, 4, 5, 6}

# range(0, len(s))
s.remove(4)
print(s)
