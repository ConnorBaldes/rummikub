class Graph:
    def __init__(self, size):
        self.size = size
        self.edges = []  # List of edges (weight, u, v)
        self.vertex_data = [''] * size  # Store vertex names
        self.edge_map = {}  # Fast lookup for edge weights

    def add_edge(self, u, v, weight):
        if 0 <= u < self.size and 0 <= v < self.size:
            self.edges.append((weight, u, v))  # Store (weight, u, v)
            self.edge_map[(u, v)] = weight
            self.edge_map[(v, u)] = weight  # Undirected graph

    def update_edge_weight(self, u, v, new_weight):
        """ Updates the weight of an existing edge efficiently. """
        if (u, v) in self.edge_map:
            self.edge_map[(u, v)] = new_weight
            self.edge_map[(v, u)] = new_weight

            # Update the edge list in O(E) time
            for i in range(len(self.edges)):
                weight, node1, node2 = self.edges[i]
                if (node1, node2) == (u, v) or (node1, node2) == (v, u):
                    self.edges[i] = (new_weight, u, v)
                    break
        else:
            print(f"Edge {u}-{v} does not exist.")


    def add_vertex_data(self, vertex, data):
        if 0 <= vertex < self.size:
            self.vertex_data[vertex] = data

    def find(self, parent, i):
        if parent[i] == i:
            return i
        parent[i] = self.find(parent, parent[i])  # Path compression
        return parent[i]

    def union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)

        if xroot != yroot:
            if rank[xroot] < rank[yroot]:
                parent[xroot] = yroot
            elif rank[xroot] > rank[yroot]:
                parent[yroot] = xroot
            else:
                parent[yroot] = xroot
                rank[xroot] += 1

    def kruskals_msf(self, max_weight):
        """ Computes the minimum spanning forest with a max weight threshold. """
        self.edges.sort()  # Sort edges by weight
        parent = list(range(self.size))
        rank = [0] * self.size

        forests = []
        edge_used = set()

        for weight, u, v in self.edges:
            if weight > max_weight:
                continue  # Ignore edges exceeding max_weight

            set_u = self.find(parent, u)
            set_v = self.find(parent, v)

            if set_u != set_v:
                self.union(parent, rank, set_u, set_v)
                edge_used.add((u, v, weight))

        # Group edges into separate forests
        forest_map = {}
        for vertex in range(self.size):
            root = self.find(parent, vertex)
            if root not in forest_map:
                forest_map[root] = []
            forest_map[root].append(vertex)

        for root, vertices in forest_map.items():
            forest_edges = [(u, v, w) for u, v, w in edge_used if u in vertices or v in vertices]
            forests.append((vertices, forest_edges))

        return forests

    def print_forests(self, forests):
        print('Active Sets: ')
        for i, (vertices, edges) in enumerate(forests):
            print( [self.vertex_data[v] for v in vertices])
        print()

# 175
