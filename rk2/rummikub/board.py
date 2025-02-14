import pygame
from rummikub.tile import Tile
from rummikub.utils import Graph
from typing import List, Optional


class Board:
    def __init__(self, game):
        self.game = game
        self.graph: Graph = Graph(len(self.game.deck))
        self.added_tiles: List[Tile] = []

    def add_tile(self, tile: Tile) -> None:
        """Adds a tile to the board and updates its position in the graph."""
        self.graph.add_tile(tile)
    
    def remove_tile(self, tile_id: int) -> int:
        """Removes tile added to the board via its id."""
        return self.graph.remove_tile_by_id(tile_id)
    
    def draw(self, screen) -> None:
        """Draws all tiles currently on the board."""
        for tile_id in self.graph.tile_stack:
            tile = self.game.get_tile_by_id(tile_id)
            if tile:
                tile.draw_tile(screen)
    
    def update_sets(self) -> None:
        """Updates sets by finding connected tile groups using Kruskal's algorithm."""
        forests = self.graph.kruskals_msf(max_weight=175)
        self.graph.print_forests(forests)

    def validate_sets(self) -> bool:
        return True
        # TO DO: Check that all forests in graph are either set or run 

    def pop_added(self) -> None:
        """Remove tiles added to board by current player and return them to
           players rack."""
        for tile_id in self.added_tiles:
            tile = self.graph.remove_last_tile()
            self.game.players[tile_id] = tile
            self.game.players[tile_id].reset_coordinates()

    def reset_board(self) -> None:
        self.graph.reset_tile_coordinates()
        self.graph.update_distances()

    def reset_invalid_turn(self):
        self.pop_added()
        self.reset_board()