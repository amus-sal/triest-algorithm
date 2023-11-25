from time import sleep

class Graph:

    def __init__(self):
        self.adjacency_list = {}
        self.edge_set = set()

    def hasNode(self, node):
        return node in self.adjacency_list
    
    def addNode(self, node):
        if node not in self.adjacency_list:
            self.adjacency_list[node] = set()
            
    def addEdge(self, edge):
        if edge in self.edge_set or ((edge[1], edge[0])) in self.edge_set:
            return
        self.adjacency_list[edge[0]].add(edge[1])
        self.adjacency_list[edge[1]].add(edge[0])
        self.edge_set.add((edge[0], edge[1]))
        self.edge_set.add((edge[1], edge[0]))


    def removeEdge(self, edge):
        self.adjacency_list[edge[0]].remove(edge[1])
        self.adjacency_list[edge[1]].remove(edge[0])
        self.edge_set.remove((edge[0], edge[1]))
        self.edge_set.remove((edge[1], edge[0]))

    def getEdges(self):
        return list(self.edge_set)
    
    def getNeighbors(self, u):
        return self.adjacency_list.get(u)
