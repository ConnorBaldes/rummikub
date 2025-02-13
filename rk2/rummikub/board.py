import pygame
from rummikub.tile import Tile
from rummikub.utils import Graph, DistanceMatrix
from typing import List, Optional

class Board:
    def __init__(self):
        self.graph = self._build_graph()
        self.tile_stack: List[int] = []


    def _build_graph(self) -> Graph:
        for tile in self.deck.tiles:
            self.graph.add_vertex_data(tile.id, tile)
        for tile in self.deck.tiles:
            for other_tile in self.deck.tiles:
                if tile != other_tile:
                    self.graph.add_edge(tile.id, other_tile.id, 0)
    
    def add_tile(self, tile: Tile) -> None:
        self.graph.vertex_data[tile.id] = tile
        self.tile_stack.append(tile.id)
    
    def remove_tile(self, tile: Tile) -> None:
        if tile.id in self.tile_stack:
            self.tile_stack.remove(tile.id)
            self.graph.vertex_data[tile.id] = ''
    
    def draw(self, screen) -> None:
        for tile_id in self.tile_stack:
            tile = self.graph.vertex_data[tile_id]
            if tile:
                tile.draw_tile(screen)

    def update_distances(self, distance_matrix):
        for edge in self.graph.edges:
            self.graph.update_edge_weight(edge[1], edge[2], distance_matrix[edge[1]][edge[2]])
    
    def get_tile_position(self, tile):
        return (tile.rect.x, tile.rect.y)
    
    def are_close(self, tile1, tile2, x=170, y=70):
        x1, y1 = self.get_tile_position(tile1)
        x2, y2 = self.get_tile_position(tile2)
        return (abs(x1 - x2) <= x) and (abs(y1 - y2) <= y)
    
    def update_sets(self):
        new_sets = []
        for tile in self.deck.tiles:
            found_set = None
            for tile_set in new_sets:
                if any(self.are_close(tile, t) for t in tile_set):
                    tile_set.add(tile)
                    found_set = tile_set
                    break
            if found_set is None:
                new_sets.append({tile})
        
        merged = []
        while new_sets:
            current_set = new_sets.pop()
            merged_current_set = False
            for other_set in new_sets:
                if current_set & other_set:
                    other_set.update(current_set)
                    merged_current_set = True
                    break
            if not merged_current_set:
                merged.append(current_set)
        
        self.sets = merged
    
    def draw(self, screen):
        for tile in self.deck.tiles:
            tile.draw_tile(screen)