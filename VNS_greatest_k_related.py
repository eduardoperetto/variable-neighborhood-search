import random
import graph_tools
from problem_instance import *

def greatest_k_related(instance: ProblemInstance, num_neighborhoods, max_iterations: int = 100):
    k_related_subgraph = graph_tools.get_k_related_subgraph(instance)
    best_solution = k_related_subgraph.nodes
    neighborhood = 1
    iterations = 0

    while iterations < max_iterations and neighborhood <= num_neighborhoods and len(best_solution) - neighborhood > instance.k:
        new_subgraph, _ = graph_tools.remove_nodes(make_subgraph(k_related_subgraph, best_solution), neighborhood)
        candidate_solution = new_subgraph.nodes
        candidate_solution = graph_tools.get_k_related_nodes(make_subgraph(k_related_subgraph, new_subgraph.nodes))
        if graph_tools.is_subgraph_k_related(candidate_solution, new_subgraph) and len(candidate_solution) > instance.k and graph_tools.is_better(candidate_solution, best_solution):
            best_solution = candidate_solution
            neighborhood = 1  # Go back to the first neighborhood
        else:
            neighborhood += 1
        iterations += 1

    return best_solution, iterations
