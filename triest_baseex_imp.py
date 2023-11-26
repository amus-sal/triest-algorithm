import random

import numpy as np

from graphex import Graph


class TriestBase:

    def __str__(self):
        return f'Global_triangles_counter: {self.global_triangles_counter} \n Local triangles: {self.local_triangle_counters}'

    def calculate_estimation(self):
        x_nominator = self.timestamp * (self.timestamp-1)*(self.timestamp-2)
        x_denominator = self.sample_size * ( self.sample_size-1 ) * (self.sample_size -2)

        x_t = max(1, x_nominator /x_denominator)
        triangles_per_node = {}
        for k,v in self.local_triangle_counters.items():
            triangles_per_node[k] = v * x_t 

        triangles_global = self.global_triangles_counter
        return triangles_per_node, triangles_global

    def __init__(self, memory_size):
        assert memory_size > 6
        self.graph = Graph()
        self.sample_size = memory_size
        self.timestamp = 0

        # counters
        self.local_triangle_counters = {}
        self.global_triangles_counter = 0


    def update_graph(self, edge):
        self.graph.addNode(edge[0])
        self.graph.addNode(edge[1])
        self.graph.addEdge(edge)

    def calculate_triangles(self, stream):
        triangles_per_node, triangles_global = 0, {}
        for edge in stream():
            #print(f"edge on stream: {edge}")
            self.timestamp += 1
            self.update_counters("add", edge)
            if self.sample_edge(edge, self.timestamp):
                self.update_graph(edge)


            triangles_per_node, triangles_global = self.calculate_estimation()
            #print(f"timestamp: {self.timestamp}, triangles_per_node: {triangles_per_node}, triangles_global: {triangles_global}")
            #print("***************")
        triangles_per_node, triangles_global = self.calculate_estimation()
        return triangles_global, triangles_per_node

    def sample_edge(self, edge, timestamp) -> bool:
        current_prob = self.sample_size / timestamp
        #print("timestamp: ", timestamp)
        if timestamp <= self.sample_size:
             return True
        elif random.random() <= current_prob:
            edge_list = self.graph.getEdges()
            edge_to_remove = random.choice(edge_list)
            self.graph.removeEdge(edge_to_remove)
            return True
        else:
            return False

    def update_counters(self, operation, edge):
        (u, v) = edge
        if self.graph.getNeighbors(u) or self.graph.getNeighbors(v):
            return

        #print("edge to update counters: ", edge)
        u_neighbors = self.graph.getNeighbors(u)
        v_neighbors = self.graph.getNeighbors(v)
        common_neighbors = u_neighbors & v_neighbors
        weight = max(1,((self.timestamp-1)*(self.timestamp-2))/(self.sample_size * (self.sample_size -1)))
        for c in common_neighbors:
            #print(f"operation {operation} on : ", c)
            self.global_triangles_counter += weight
            try:
                self.local_triangle_counters[c] += weight
            except:
                self.local_triangle_counters[c] = weight
            try:
                self.local_triangle_counters[u] += weight
            except:
                self.local_triangle_counters[u] = weight
            try:
                self.local_triangle_counters[v] += weight
            except:
                self.local_triangle_counters[v] = weight
                
            # print(f"result on {c}: ", self.local_triangle_counters[c])
            # print(f"result on {u}: ", self.local_triangle_counters[u])
            # print(f"result on {v}: ", self.local_triangle_counters[v])

        return None



