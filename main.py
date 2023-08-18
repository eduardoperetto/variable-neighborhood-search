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

# Greedy algorithm to iteratively remove vertices with the fewest neighbors until the required number of vertices (p) are removed. 
def local_search(instance):
    selected_vertices = set(range(1, instance.n + 1))
    for _ in range(instance.p):
        # Find the vertex with the least neighbors among the selected vertices
        vertex_with_least_neighbors = min(selected_vertices, key=lambda v: count_neighbors(v, selected_vertices, instance.edges))
        selected_vertices.remove(vertex_with_least_neighbors)

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

if __name__ == '__main__':
    solution = variable_neighborhood_search(extract_instance_from_txt())
    print(f"\nSubset of vertices to remove from network: {solution}")
