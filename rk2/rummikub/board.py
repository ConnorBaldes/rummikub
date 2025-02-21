import pygame
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
        forests = self.graph.kruskals_msf(self.tiles, max_weight=175)
        #print(forests)
        self.graph.print_forests(forests)

    def validate_sets(self) -> bool:
        self.added_tiles = []
        return True
        # TO DO: Check that all forests in graph are either set or run 

    def reset_board(self) -> None:
        self.graph.reset_tile_coordinates()
        self.graph.update_distances()

    def get_tile_positions(self):

        tile_positions = {}
        for tile in self.added_tiles: 
            tile_positions[tile.id] = (tile.rect.x, tile.rect.y)
        return tile_positions