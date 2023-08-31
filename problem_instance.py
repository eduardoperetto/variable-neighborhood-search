from copy import deepcopy

class ProblemInstance:
    def __init__(self, nodes, k, p, edges):
        self.nodes = nodes
        self.k = k
        "k is the maximum number of relations each node of the subset can have"
        self.p = p
        "p is the length of the subset of 'important' individuals to remove from the network"
        self.edges = edges

    def __str__(self):
        return f"ProblemInstance(nodes={self.nodes}, k={self.k}, p={self.p}, edges={self.edges})"
    
    def copy(self):
             return deepcopy(self)

def make_subgraph(previous_instance, subset):
        new_instance = deepcopy(previous_instance)
        new_instance.nodes = subset
        return new_instance