
import numpy as np
import pygame
from typing import Dict, Tuple, List
from rummikub.tile import Tile


import numpy as np

import numpy as np

class Graph:
    """Optimized adjacency matrix representation of the playing board.
       This version works with an external dictionary of board tiles.
    """
    def __init__(self, max_size: int):
        self.size = max_size
        # Distance matrix: initialize with infinity, diagonal set to 0.
        self.matrix = np.full((self.size, self.size), np.inf)
        np.fill_diagonal(self.matrix, 0)
        # Vertex data: Each row holds [x, y, tile_id]. Uninitialized rows are [-1, -1, -1].
        self.vertex_data = np.full((self.size, 3), -1, dtype=int)
    
    def add_tile(self, tile):
        """Add a new tile to the graph. If the tile already exists,
           update its data; otherwise, register it as active.
        """
        tid = tile.get_id()
        # Check if the tile is already active (i.e. vertex_data[tid] not all -1).
        if (self.vertex_data[tid] != -1).all():
            self.update_tile(tile)
            return
        # Set tile's current position.
        self.vertex_data[tid] = [tile.get_x(), tile.get_y(), tid]
        # Find all active tile indices.
        active_indices = np.where(self.vertex_data[:, 0] != -1)[0]
        # Compute new tile distances relative to active ones.
        coords = self.vertex_data[active_indices, :2].astype(float)
        tile_coords = np.array(self.vertex_data[tid, :2], dtype=float)
        diff = coords - tile_coords
        distances = np.sqrt(np.sum(diff ** 2, axis=1))
        # Update the row and column corresponding to tile 'tid'.
        self.matrix[tid, active_indices] = distances
        self.matrix[active_indices, tid] = distances
        np.fill_diagonal(self.matrix, 0)
    
    def update_tile(self, tile):
        """Update vertex data and distances for a single tile.
           Should be called after the tile moves.
        """
        tid = tile.get_id()
        self.vertex_data[tid] = [tile.get_x(), tile.get_y(), tid]
        coords = self.vertex_data[:, :2].astype(float)
        tile_coords = np.array(self.vertex_data[tid, :2], dtype=float)
        diff = coords - tile_coords
        distances = np.sqrt(np.sum(diff ** 2, axis=1))
        self.matrix[tid, :] = distances
        self.matrix[:, tid] = distances
        np.fill_diagonal(self.matrix, 0)
    
    def update_all_tiles(self, tiles: dict):
        """Refresh the entire graph based on the current positions in the provided tiles dictionary.
           'tiles' is a dictionary {tile_id: Tile}.
        """
        for tile in tiles.values():
            tid = tile.get_id()
            self.vertex_data[tid] = [tile.get_x(), tile.get_y(), tid]
        coords = self.vertex_data[:, :2].astype(float)
        diff = coords[:, None, :] - coords[None, :, :]
        self.matrix = np.sqrt(np.sum(diff ** 2, axis=2))
        np.fill_diagonal(self.matrix, 0)
    
    def reset_tile_data(self, tile_id: int):
        """Resets the vertex data and distances for a removed tile."""
        self.vertex_data[tile_id] = [-1, -1, -1]
        self.matrix[tile_id, :] = np.inf
        self.matrix[:, tile_id] = np.inf
        np.fill_diagonal(self.matrix, 0)
    
    def remove_tile_by_id(self, tile_id: int) -> bool:
        """Removes a specific tile from the graph and resets its data.
           Returns True if removal was successful.
        """
        if (self.vertex_data[tile_id] == -1).all():
            return False
        self.reset_tile_data(tile_id)
        return True
    
    def kruskals_msf(self, active_tiles: dict, max_weight: float):
        """Computes a minimum spanning forest with a max weight threshold.
           'active_tiles' is a dictionary {tile_id: Tile}.
        """
        active_ids = np.array(list(active_tiles.keys()), dtype=int)
        if active_ids.size == 0:
            return []
        
        submatrix = self.matrix[np.ix_(active_ids, active_ids)]
        triu_idx = np.triu_indices_from(submatrix, k=1)
        edges = np.column_stack((active_ids[triu_idx[0]], active_ids[triu_idx[1]]))
        weights = submatrix[triu_idx]
        
        valid = weights <= max_weight
        edges, weights = edges[valid], weights[valid]
        sorted_indices = np.argsort(weights)
        edges, weights = edges[sorted_indices], weights[sorted_indices]
        
        parent = np.arange(self.size)
        rank = np.zeros(self.size, dtype=int)
        
        def find(i):
            if parent[i] != i:
                parent[i] = find(parent[i])
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
        
        forest_map = {}
        for tid in active_ids:
            root = find(tid)
            if root not in forest_map:
                forest_map[root] = []
            forest_map[root].append(tid)
        
        forests = [(vertices, [(u, v, self.matrix[u, v])
                    for u, v, _ in edge_used if u in vertices or v in vertices])
                   for vertices in forest_map.values()]
        return forests
    
    def print_forests(self, forests):
        """Display the current grouped sets of active tiles."""
        print('Active Sets:')
        for vertices, edges in forests:
            print('{', [self.vertex_data[v][2] for v in vertices], '}')
