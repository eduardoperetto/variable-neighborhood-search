class ProblemInstance:
    def __init__(self, n, m, k, p, edges):
        self.n = n
        self.m = m
        self.k = k
        self.p = p
        self.edges = edges

    def __str__(self):
        return f"ProblemInstance(n={self.n}, m={self.m}, k={self.k}, p={self.p}, edges={self.edges})"


def extract_instance_from_txt(file_path: str = "source.txt"):
    with open(file_path, 'r') as file:
        n, m, k, p = map(int, file.readline().split())
        edges = []
        for _ in range(m):
            u, v = map(int, file.readline().split())
            edges.append((u, v))
    return ProblemInstance(n, m, k, p, edges)

def variable_neighborhood_search(instance):
    print(instance)

if __name__ == '__main__':
    variable_neighborhood_search(extract_instance_from_txt())
