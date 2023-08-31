import random
from time import time
import itertools

import graph_tools
from problem_instance import *
from VNS_greatest_k_related import greatest_k_related

TIME_LIMIT_IN_SECONDS = 50

# Check readme for details about how to make a .txt source file
def extract_instance_from_txt(file_path: str = "source.txt"):
    with open(file_path, 'r') as file:
        n, m, k, p = map(int, file.readline().split())
        edges = []
        for _ in range(m):
            u, v = map(int, file.readline().split())
            edges.append((u, v))
    
    instance = ProblemInstance(range(1, n + 1), k, p, edges)
    print(f"Successfully read instance from file:\n{instance}")
    return instance

# Main function to search the graph's K most important individuals in the ProblemInstance using VNS.
def minimize_k_related_subset(instance, num_neighborhoods):
    k_related_subset = graph_tools.get_k_related_nodes(instance)
    global_best_solution = k_related_subset.copy()
    optimal_individuals_to_remove = []
    last_improve_iterations = num_iterations = 0
    start_time = time()

    max_iterations_without_improve = len(instance.nodes) * 100
    
    while num_iterations - last_improve_iterations < max_iterations_without_improve:
        if time() - start_time > TIME_LIMIT_IN_SECONDS:
            print("Reached time limit!")
            break

        # Generate new subgraph by taking the graph being searched and removing 'p' nodes
        new_subgraph, nodes_to_remove = graph_tools.remove_nodes(make_subgraph(instance, k_related_subset), instance.p)

        # Apply VNS to solve the greatest K related subset within the new subgraph
        candidate, new_iterations = greatest_k_related(new_subgraph, num_neighborhoods, max_iterations=25)
        num_iterations += new_iterations

        if graph_tools.is_better(candidate, global_best_solution):
            global_best_solution = candidate
            last_improve_iterations = num_iterations
            optimal_individuals_to_remove = nodes_to_remove

    print(f"Finished running. Time elapsed: {time() - start_time} | num of iterations: {num_iterations}")
            
    return global_best_solution, optimal_individuals_to_remove

if __name__ == '__main__':
    instance = extract_instance_from_txt('examples/source.txt')
    min_k_related_subset, optimal_removed = minimize_k_related_subset(instance, num_neighborhoods=1)
    print(f"\nMinimum subset {instance.k}-related: {min_k_related_subset} | Length of the subset: {len(min_k_related_subset)}")
    print(f"Optimal individuals to remove: {optimal_removed}")
    graph_tools.draw_graph(instance, min_k_related_subset, optimal_removed)
