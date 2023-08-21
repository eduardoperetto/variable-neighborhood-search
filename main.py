import networkx as nx
import matplotlib.pyplot as plt

class ProblemInstance:
    def __init__(self, n, m, k, p, edges):
        self.n = n
        self.m = m
        self.k = k
        self.p = p
        self.edges = edges

    def __str__(self):
        return f"ProblemInstance(n={self.n}, m={self.m}, k={self.k}, p={self.p}, edges={self.edges})"

# Helper function to count neighbors of a vertex
def count_neighbors(vertex, selected_vertices, edges):
    count = 0
    for u, v in edges:
        if u == vertex and v in selected_vertices:
            count += 1
        elif v == vertex and u in selected_vertices:
            count += 1
    return count

def remove_vertices(selected_vertices, num_vertices):
    return set(sorted(selected_vertices)[:-num_vertices])

# Greedy algorithm to iteratively remove vertices with the fewest neighbors until the required number of vertices (p) are removed. 
def local_search(instance):
    selected_vertices = set(range(1, instance.n + 1))
    neighborhood_levels = [1, 2, 3]

    for level in neighborhood_levels:
        num_vertices_to_remove = level
        
        while num_vertices_to_remove <= instance.p:
            current_solution = remove_vertices(selected_vertices, num_vertices_to_remove)
            improved = False
            
            while not improved:
                next_solution = remove_vertices(current_solution, 1)
                
                # Check if the new solution is better
                if count_neighbors(next_solution.pop(), next_solution, instance.edges) <= instance.k:
                    current_solution = next_solution
                    improved = True
                else:
                    break
            
            # If an improved solution is found, restart the search from the first neighborhood
            if improved:
                num_vertices_to_remove = 1
            else:
                num_vertices_to_remove += 1
        
        selected_vertices = current_solution
    
    return selected_vertices

def extract_instance_from_txt(file_path: str = "source.txt"):
    with open(file_path, 'r') as file:
        n, m, k, p = map(int, file.readline().split())
        edges = []
        for _ in range(m):
            u, v = map(int, file.readline().split())
            edges.append((u, v))
    instance = ProblemInstance(n, m, k, p, edges)
    print(f"Successfully read instance from file:\n\t{instance}")
    return instance

def variable_neighborhood_search(instance):
    selected_vertices = local_search(instance)
    return selected_vertices

# Helper function to draw the graph in the screen. Not recomended for large instances
def draw_graph(instance: ProblemInstance, colored):
    G = nx.Graph()
    G.add_nodes_from(range(1, instance.n + 1))
    G.add_edges_from(instance.edges)
    node_colors = ['red' if node in colored else 'blue' for node in G.nodes()]

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=1000, font_size=10, font_color='black', node_color=node_colors)
    plt.show()

if __name__ == '__main__':
    instance = extract_instance_from_txt()
    solution = variable_neighborhood_search(instance)
    draw_graph(instance, solution)
    print(f"\nSubset of vertices to remove from network: {solution}")
