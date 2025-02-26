import pygame
import math
from rummikub.tile import Tile
from rummikub.utils import Graph
from typing import List, Optional


class Board:
    def __init__(self, game):
        self.game = game
        self.graph: Graph = Graph(106)
        self.tiles = {} # All board tiles: {tile_id: Tile}
        self.added_tiles = [] # Tile IDs added during current turn

    def add_tile(self, tile: Tile) -> None:
        self.tiles[tile.id] = tile
        self.added_tiles.append(tile.id)

        # Update board graph
        self.graph.add_tile(tile)
    
    def remove_tile(self, tile_id: int):
        # Only reversible if the tile was added on the current turn
        if tile_id in self.added_tiles:
            self.added_tiles.remove(tile_id)
            self.graph.remove_tile_by_id(tile_id)
            return self.tiles.pop(tile_id)
        
        return None
    
    def draw(self, screen) -> None:
        for tile in self.tiles.values():
            tile.draw(screen)
    

    def update_sets(self) -> None:
        """Updates sets by finding connected tile groups using Kruskal's algorithm."""
        self.graph.update_all_tiles(self.tiles)
        forests = self.graph.kruskals_msf(self.tiles, max_weight=200)
        self.graph.print_forests(forests)

    def snap_tile(self, dropped_tile: Tile, snap_threshold: float = 200) -> None:
        """
        Snap dropped_tile horizontally so that it aligns to the left or right side
        of the nearest tile, creating a row.
        Assumes tile dimensions are 140px wide and 240px tall.
        """
        # Get the nearest neighbor info from the graph.
        nearest_id, nearest_distance = self.graph.get_nearest_neighbor(dropped_tile)
        if nearest_distance >= snap_threshold:
            return  # No snapping if too far away.
        
        nearest_tile = self.tiles.get(nearest_id)
        if not nearest_tile:
            return

        # Compute candidate positions:
        # Candidate to snap on the left side of nearest_tile:
        candidate_left = (nearest_tile.get_x() - dropped_tile.rect.width, nearest_tile.get_y())
        # Candidate to snap on the right side of nearest_tile:
        candidate_right = (nearest_tile.get_x() + nearest_tile.rect.width, nearest_tile.get_y())

        # Compute distance from the dropped tile's current position to each candidate.
        current_pos = dropped_tile.get_coordinates()
        dist_left = math.hypot(current_pos[0] - candidate_left[0],
                               current_pos[1] - candidate_left[1])
        dist_right = math.hypot(current_pos[0] - candidate_right[0],
                                current_pos[1] - candidate_right[1])

        # Choose the candidate with the smaller distance.
        best_candidate = candidate_left if dist_left < dist_right else candidate_right

        # Snap the dropped tile.
        dropped_tile.set_coordinates(best_candidate[0], best_candidate[1])
        # Update the graph for the dropped tile.
        self.graph.update_tile(dropped_tile)


    def validate_sets(self) -> bool:
        self.added_tiles = []
        return True
        # TO DO: Check that all forests in graph are either set or run 

    def reset_board(self) -> None:
        self.graph.reset_tile_coordinates()
        self.graph.update_distances()

    def get_tile_positions(self):

        tile_positions = {}
        for tile in self.tiles: 
            tile_positions[tile.id] = (tile.rect.x, tile.rect.y)
        return tile_positions
    
