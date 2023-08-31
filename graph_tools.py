import networkx as nx
import matplotlib.pyplot as plt
from problem_instance import *
import random

# Helper function to draw the graph in the screen. Not recomended for large instances
def draw_graph(instance: ProblemInstance, selected: list, removed: tuple):
    G = nx.Graph()
    G.add_nodes_from(instance.nodes)
    G.add_edges_from(instance.edges)
    
    node_colors = []
    for node in G.nodes():
        if node in selected:
            node_colors.append('green')
        elif node in removed:
            node_colors.append('red')
        else:
            node_colors.append('blue')

    pos = nx.kamada_kawai_layout(G)
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=1000,
        font_size=10,
        font_color='black',
        node_color=node_colors
    )
    plt.show()

def is_node_k_related(node: int, instance: ProblemInstance):
    count = 0
    for edge in instance.edges:
        if edge[0] == node and edge[1] in instance.nodes:
            count += 1
        elif edge[1] == node and edge[0] in instance.nodes:
            count += 1
    return count >= instance.k

def get_k_related_nodes(instance: ProblemInstance) -> list:
    k_related_nodes = [node for node in instance.nodes if is_node_k_related(node, instance)]
    return k_related_nodes

def get_k_related_subgraph(instance: ProblemInstance) -> ProblemInstance:
    k_related_nodes = [node for node in instance.nodes if is_node_k_related(node, instance)]
    return make_subgraph(instance, k_related_nodes)

def is_subgraph_k_related(subset: list, instance: ProblemInstance) -> bool:
    for node in subset:
        if not is_node_k_related(node, make_subgraph(instance, subset)):
            return False
    return True

def is_better(rhs_nodes: list, lhs_nodes: list):
    return len(rhs_nodes) < len(lhs_nodes)

def remove_nodes(instance, num_nodes):
    nodes_to_remove = random.sample(instance.nodes, num_nodes)
    new_nodes = [node for node in instance.nodes if node not in nodes_to_remove]
    return make_subgraph(instance, new_nodes), nodes_to_remove
