class UnionFind:
    """Union-Find data structure with path compression and union by rank."""
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])  # Path compression
        return self.parent[u]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u != root_v:
            # Union by rank
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1


def kruskal_with_exclusion(n, edges, exclude_edge1=None, exclude_edge2=None):
    """Kruskal's algorithm to find MST, optionally excluding one edge."""
    uf = UnionFind(n)
    mst_weight = 0
    edge_count = 0
    mst_edges = []

    for weight, u, v in edges:
        # Skip the excluded edge
        if exclude_edge1 and (u == exclude_edge1[0] and v == exclude_edge1[1] or u == exclude_edge1[1] and v == exclude_edge1[0]):
            continue
        if exclude_edge2 and (u == exclude_edge2[0] and v == exclude_edge2[1] or u == exclude_edge2[1] and v == exclude_edge2[0]):
            continue
        if uf.find(u) != uf.find(v):
            uf.union(u, v)
            mst_weight += weight
            mst_edges.append((u, v))
            edge_count += 1
            if edge_count == n - 1:  # MST is complete
                break

    if edge_count == n - 1:
        return mst_weight, mst_edges
    else:
        return float('inf'), []


def find_msts(n, adjacency_matrix):
    """Find the weights of the first, second, and third MSTs."""
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if adjacency_matrix[i][j] >= 0:
                edges.append((adjacency_matrix[i][j], i, j))
    edges.sort()  # Sort edges by weight for Kruskal's algorithm

    first, first_mst_edges = kruskal_with_exclusion(n, edges)

    second = float('inf')
    second_edges = []
    for edge in first_mst_edges:
        test, test_edges = kruskal_with_exclusion(n, edges, edge)
        if test < second:
            second = test
            second_edges = test_edges

    third = float('inf')
    for edge1 in first_mst_edges:
        for edge2 in second_edges:
            test, test_edges = kruskal_with_exclusion(n, edges, edge1, edge2)
            if test < third:
                third = test

    return first, second, third


def read_graph_from_file(filename):
    """Reads the graph from a file and returns the number of vertices and the adjacency matrix."""
    with open(filename, 'r') as file:
        lines = file.readlines()
        n = int(lines[0].strip())  # First line contains the number of vertices
        adjacency_matrix = [
            list(map(int, line.strip().split(','))) for line in lines[1:]
        ]
    return n, adjacency_matrix


def write_results_to_file(filename, m1, m2, m3):
    """Writes the results (MST weights) to a file."""
    with open(filename, 'w+') as file:
        file.write(f"{m1}\n{m2}\n{m3}\n")


def three_min_spanning_trees(input_file_path, output_file_path):
    n, adjacency_matrix = read_graph_from_file(input_file_path)
    m1, m2, m3 = find_msts(n, adjacency_matrix)
    write_results_to_file(output_file_path, m1, m2, m3)


def main():
    # Example: Test files
    test_files = ["test1.txt", "test2.txt"]

    for test_file in test_files:
        n, adjacency_matrix = read_graph_from_file(test_file)
        m1, m2, m3 = find_msts(n, adjacency_matrix)
        output_file = f"{test_file.split('.')[0]}_results.txt"
        write_results_to_file(output_file, m1, m2, m3)


if __name__ == "__main__":
    main()
