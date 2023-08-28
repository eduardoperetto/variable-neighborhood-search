import networkx as nx
import matplotlib.pyplot as plt
import itertools
import random
from time import time

TIME_LIMIT_IN_SECONDS = 30

class ProblemInstance:
    def __init__(self, n, m, k, p, edges):
        self.n = n
        "n is the number of vertices in the graph"
        self.m = m
        "m is the number of edges"
        self.k = k
        "k is the maximum number of relations each node of the subset can have"
        self.p = p
        "p is the length of the subset of 'important' individuals to remove from the network"
        self.edges = edges

    def __str__(self):
        return f"ProblemInstance(n={self.n}, m={self.m}, k={self.k}, p={self.p}, edges={self.edges})"
    
    def is_k_related(self, subset):
        for node in subset:
            if not is_node_k_related(node, subset, self):
                return False
        return True

# Check readme for details about how to make a .txt source file
def extract_instance_from_txt(file_path: str = "source.txt"):
    with open(file_path, 'r') as file:
        n, m, k, p = map(int, file.readline().split())
        edges = []
        for _ in range(m):
            u, v = map(int, file.readline().split())
            edges.append((u, v))
    instance = ProblemInstance(n, m, k, p, edges)
    print(f"Successfully read instance from file:\n{instance}")
    return instance

# Helper function to draw the graph in the screen. Not recomended for large instances
def draw_graph(instance: ProblemInstance, colored):
    G = nx.Graph()
    G.add_nodes_from(range(1, instance.n + 1))
    G.add_edges_from(instance.edges)
    node_colors = ['red' if node in colored else 'blue' for node in G.nodes()]

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=1000, font_size=10, font_color='black', node_color=node_colors)
    plt.show()

def is_node_k_related(node, subset, instance):
    count = 0
    for edge in instance.edges:
        if edge[0] == node and edge[1] in subset:
            count += 1
        elif edge[1] == node and edge[0] in subset:
            count += 1
    return count >= instance.k

def local_search(subset, best_solution, num_nodes_to_remove, instance):
    node_combinations_to_remove = list(itertools.combinations(subset, num_nodes_to_remove))
    # random.shuffle(node_combinations_to_remove)

    for node_combination_to_remove in node_combinations_to_remove:
        new_subset = [node for node in subset if node not in node_combination_to_remove]
        
        if instance.is_k_related(new_subset):
            if len(new_subset) < len(best_solution):
                best_solution = new_subset
                print(f"Subset is better! {best_solution}")
                break

    return best_solution

# Main function to search the graph's K most important individuals in the ProblemInstance using VNS.
def vns(problem_instance, num_neighborhoods):
    k_related_nodes = [node for node in range(problem_instance.n + 1) if is_node_k_related(node, range(problem_instance.n), problem_instance)]
    
    # Remove nodes with less than k relations
    k_related_subset = [node for node in k_related_nodes if is_node_k_related(node, k_related_nodes, problem_instance)]
    print(f"K-related nodes: {k_related_subset}")

    # Initial solution is all the k-related nodes in the graph
    best_solution = k_related_subset
    neighborhood_level = 1
    
    start_time = time()
    
    # Searching until algorithm has searched through all neighborhoods or has reached time limit
    while neighborhood_level <= num_neighborhoods and (time() - start_time < TIME_LIMIT_IN_SECONDS):
        print(f"Processing neighborhood level {neighborhood_level}")
        
        new_best_solution = local_search(k_related_subset, best_solution, neighborhood_level, problem_instance)

        if new_best_solution != best_solution:
            neighborhood_level = 1
            best_solution = new_best_solution
        else:
            neighborhood_level += 1
            
    return best_solution

if __name__ == '__main__':
    instance = extract_instance_from_txt('source.txt')
    solution = vns(instance, num_neighborhoods=13)
    # draw_graph(instance, solution)
    print(f"\nMinimum subset {instance.k}-related: {solution}")
    print(f"Length of the subset: {len(solution)}")