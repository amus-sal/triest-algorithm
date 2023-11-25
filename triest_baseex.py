import random

import numpy as np

from graphex import Graph


class TriestBase:

    def __str__(self):
        return f'Global_triangles_counter: {self.global_triangles_counter} \n Local triangles: {self.local_triangle_counters}'
    def __init__(self, memory_size):
        assert memory_size >= 6
        self.graph = Graph()
        self.sample_size = memory_size
        self.timestamp = 0

        # counters
        self.local_triangle_counters = {}
        self.global_triangles_counter = 0

    def update_sample(self, edge):
        self.graph.addEdge(edge)
        if not self.local_triangle_counters.get(edge[0]):
            self.local_triangle_counters[edge[0]] = 0
        if not self.local_triangle_counters.get(edge[1]):
            self.local_triangle_counters[edge[1]] = 0


    def calculate_triangles(self, stream):
        for edge in stream():
            print(edge)
            if not self.graph.hasNode(edge[0]):
                self.graph.addNode(edge[0])
            if not self.graph.hasNode(edge[1]):
                self.graph.addNode(edge[1])
            self.graph.addEdge(edge)
            self.timestamp += 1
            if self.sample_edge(edge, self.timestamp):
                self.update_sample(edge)
                self.update_counters("add", edge)

    def sample_edge(self, edge, timestamp) -> bool:
        current_prob = self.sample_size / timestamp
        print("timestamp: ", timestamp)
        if timestamp <= self.sample_size:
             return True
        elif random.random() <= current_prob:
            edge_list = self.graph.getEdges()
            edge_to_remove = random.choice(edge_list)
            self.graph.removeEdge(edge_to_remove)
            self.update_counters("subtract", edge_to_remove)
            return True
        else:
            return False

    def update_counters(self, operation, edge):
        (u, v) = edge
        print("edge: ", edge)
        print("operation: ", operation)
        u_neighbors = self.graph.getNeighbors(u)
        v_neighbors = self.graph.getNeighbors(v)
        common_neighbors = u_neighbors & v_neighbors
        print("Common neighbours: " ,common_neighbors)
        for c in common_neighbors:
            print("operation on : ", c)
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
                
            print(f"result on {c}: ", self.local_triangle_counters[c])
            print(f"result on {u}: ", self.local_triangle_counters[u])
            print(f"result on {v}: ", self.local_triangle_counters[v])

        return None



