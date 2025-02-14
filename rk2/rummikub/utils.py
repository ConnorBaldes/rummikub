
import numpy as np
import pygame
from typing import Dict, Tuple, List
from rummikub.tile import Tile

class Graph:
    """Optimized adjacency matrix representation of the playing board."""

    def __init__(self, max_size: int):
        self.size = max_size
        
        # NumPy matrix for edge weights (stores Euclidean distances)
        self.matrix = np.full((self.size, self.size), np.inf)
        np.fill_diagonal(self.matrix, 0)  # Distance to itself is always 0

        # NumPy array for tile data (indexed by tile_id)
        self.vertex_data = np.full((self.size, 3), -1, dtype=int)  # Uninitialized state (-1)

        # Stack of tiles on the board
        self.tile_stack: List[Tile] = []

    def add_tile(self, tile: Tile):
        """Adds a tile to the board, initializes its vertex data, and updates edge weights."""
        if tile not in self.tile_stack:
            self.tile_stack.append(tile)
            self.vertex_data[tile.get_id()] = [tile.get_x(), tile.get_y(), tile.get_id()]
            self.update_distances(tile.id)

    def remove_last_tile(self) -> Tile:
        """Removes the last tile from the board and resets its data."""
        if self.tile_stack:
            tile = self.tile_stack.pop()
            self.reset_tile_data(tile.get_id())
            return tile
        return -1
    
    def remove_tile_by_id(self, tile_id: int) -> bool:
        """Removes a specific tile from the board and resets its data."""
        for tile in self.tile_stack:
            if tile.get_id() == tile_id:
                self.tile_stack.remove(tile)
                self.reset_tile_data(tile_id)
                return True
        return False

    def reset_tile_data(self, tile_id: int):
        """Resets the vertex data and distances of a removed tile."""
        self.vertex_data[tile_id] = [-1, -1, -1]  # Reset to uninitialized state
        self.matrix[tile_id, :] = np.inf
        self.matrix[:, tile_id] = np.inf
        np.fill_diagonal(self.matrix, 0)

    def reset_tile_coordinates(self):
        for tile in self.tile_stack:
            tile.reset_coordinates()


    def update_distances(self, tile_id: int):
        """Updates distances for a newly added tile."""
        coords = self.vertex_data[:, :2]  # Extract only x, y coordinates
        diff = coords - self.vertex_data[tile_id, :2]
        self.matrix[tile_id, :] = np.sqrt(np.sum(diff ** 2, axis=1))
        self.matrix[:, tile_id] = self.matrix[tile_id, :]

    def kruskals_msf(self, max_weight: float):
        """Computes a minimum spanning forest with a max weight threshold."""
        if not self.tile_stack:
            return []
        
        active_tiles = np.array([tile.get_id() for tile in self.tile_stack], dtype=int)
        edges = np.column_stack(np.triu_indices_from(self.matrix[active_tiles[:, None], active_tiles], 1))
        weights = self.matrix[active_tiles[edges[:, 0]], active_tiles[edges[:, 1]]]

        # Filter edges that exceed max weight
        valid = weights <= max_weight
        edges, weights = edges[valid], weights[valid]

        # Sort edges by weight
        sorted_indices = np.argsort(weights)
        edges, weights = edges[sorted_indices], weights[sorted_indices]

        # Kruskal's algorithm
        parent = np.arange(self.size)
        rank = np.zeros(self.size, dtype=int)

        def find(i):
            if parent[i] != i:
                parent[i] = find(parent[i])  # Path compression
            return parent[i]

        def union(x, y):
            root_x, root_y = find(x), find(y)
            if root_x != root_y:
                if rank[root_x] < rank[root_y]:
                    parent[root_x] = root_y
                elif rank[root_x] > rank[root_y]:
                    parent[root_y] = root_x
                else:
                    parent[root_y] = root_x
                    rank[root_x] += 1

        edge_used = []
        for u, v in edges:
            if find(u) != find(v):
                union(u, v)
                edge_used.append((u, v, self.matrix[u, v]))

        # Group edges into forests
        forest_map = {}
        for tile in self.tile_stack:
            root = find(tile.get_id())
            if root not in forest_map:
                forest_map[root] = []
            forest_map[root].append(tile.get_id())

        forests = [(vertices, [(u, v, self.matrix[u, v]) for u, v, _ in edge_used if u in vertices or v in vertices]) 
                   for vertices in forest_map.values()]
        
        return forests

    def print_forests(self, forests):
        """Display the current sets of grouped tiles."""
        print('Active Sets:')
        for i, (vertices, edges) in enumerate(forests):
            print([self.vertex_data[v] for v in vertices])
        print()
