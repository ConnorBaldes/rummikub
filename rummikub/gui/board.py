import pygame
import math
import numpy as np
from deck import Deck
from deck import Tile
from graph import Graph


class DistanceMatrix:
    """Efficiently computes and stores distances between tiles."""
    def __init__(self, tiles):
        self.tiles = tiles
        self.size = len(tiles)
        self.matrix = np.full((self.size, self.size), np.inf)  # Initialize with infinity
        np.fill_diagonal(self.matrix, 0)  # Distance to itself is 0

    def update_coordinates(self):
        """Extract updated coordinates from tiles into a NumPy array."""
        self.coordinates = np.array([self.tiles[tile].get_coordinates() for tile in self.tiles])

    

    def recompute_distances(self):
        """Vectorized recomputation of all distances."""
        self.update_coordinates()  # Refresh positions
        indices = np.arange(self.size)
        i, j = np.meshgrid(indices, indices, indexing='ij')

        # Compute Euclidean distance efficiently
        self.matrix = np.sqrt(((self.coordinates[i, 0] - self.coordinates[j, 0]) ** 2) +
                              ((self.coordinates[i, 1] - self.coordinates[j, 1]) ** 2))

    def print_matrix(self):
        """Display the matrix for debugging."""
        print(np.array_str(self.matrix, precision=2, suppress_small=True))



class Board:
    def __init__(self):

        self.screen = pygame.display.set_mode((3400, 2500))
        self.deck = Deck()
        self.distance_matrix = DistanceMatrix(self.deck.tiles)
        self.tile_graph = self._build_graph()
        self.sets = []

    def set_title(self, title= "Rummikub"):
        pygame.display.set_caption(title)



    def _build_graph(self):

        tile_graph = Graph(len(self.deck.tiles))

        for tile in range(len(self.deck.tiles)):
            tile_graph.add_vertex_data(self.deck.tiles[tile].id, data= self.deck.tiles[tile])
        for tile in range(len(self.deck.tiles)):
            for other_tile in range(len(self.deck.tiles)):
                if tile != other_tile:
                    tile_graph.add_edge(self.deck.tiles[tile].id, self.deck.tiles[other_tile].id, 0)

        return tile_graph


    def update_distances(self):
        
        for edge in self.tile_graph.edges:
            self.tile_graph.update_edge_weight(edge[1], edge[2], self.distance_matrix.matrix[edge[1], edge[2]])

    def get_forests(self, max_weight= 175):

        forests = self.tile_graph.kruskals_msf(max_weight)
        self.sets = []
        for i, (vertices, edges) in enumerate(forests):
            
            self.snap_to_forests(vertices)
            self.sets.append([self.tile_graph.vertex_data[v] for v in vertices])
        
        return forests


    def snap_to_forests(self, vertices):

        tile_positions = {v: self.tile_graph.vertex_data[v] for v in vertices}

        for v in vertices:
            x = tile_positions[v].rect.x
            y = tile_positions[v].rect.y
            min_dist = float(240) # closest existing tile in the same forest
            closest_vertex = v

            for u in vertices:
                if u == v:
                    continue
                ux = tile_positions[u].rect.x
                uy = tile_positions[u].rect.y
                dist = math.sqrt((x - ux) ** 2 + (y - uy) ** 2)
                if dist < min_dist:
                    min_dist = dist
                    closest_vertex = u

            # Snap to the closest vertex
            if closest_vertex != v:
                if self.deck.tiles[closest_vertex].rect.x > self.deck.tiles[v].rect.x:
                    self.deck.tiles[v].rect.x = (self.deck.tiles[closest_vertex].rect.x) - 141
                    self.deck.tiles[v].rect.y = (self.deck.tiles[closest_vertex].rect.y)
                elif self.deck.tiles[closest_vertex].rect.x < self.deck.tiles[v].rect.x:
                    self.deck.tiles[v].rect.x = (self.deck.tiles[closest_vertex].rect.x) + 141
                    self.deck.tiles[v].rect.y = (self.deck.tiles[closest_vertex].rect.y)
                



    def get_tile_positions(self):

        tile_positions = {}
        for tile in self.deck.tiles: 
            tile_positions[self.deck.tiles[tile].id] = (self.deck.tiles[tile].rect.x, self.deck.tiles[tile].rect.y)
        return tile_positions
    
    def get_tile_position(self, tile):
        return (self.deck.tiles[tile].rect.x, self.deck.tiles[tile].rect.y)




    def are_close(self, tile1, tile2, x=170, y=70):
        x1, y1 = self.get_tile_position(tile1)
        x2, y2 = self.get_tile_position(tile2)
        return (abs(x1 - x2) <= x) and (abs(y1 - y2) <= y)
    
    def update_sets(self):
        new_sets = []
        
        # Step 1: Group tiles into new sets based on proximity
        for tile in self.deck.tiles:
            found_set = None
            for tile_set in new_sets:
                # Check if the tile is close to any tile in the set
                if any(self.are_close(tile, t) for t in tile_set):
                    tile_set.add(tile)
                    found_set = tile_set
                    break
            
            # If the tile was not added to any set, create a new set with the tile
            if found_set is None:
                # print(f'Creating new set for {self.deck.tiles[tile].num}')
                new_sets.append({tile})

        # Step 2: Properly merge sets that have any overlap (tiles that share elements)
        merged = []
        while new_sets:
            current_set = new_sets.pop()  # Take the last set from new_sets
            merged_current_set = False  # Flag to check if we need to merge the set
            
            for other_set in new_sets:
                # Check if there's any intersection (common tile) between the current set and any other set
                if current_set & other_set:  # The & operator finds common elements
                    # Merge the sets (combine them into one)
                    other_set.update(current_set)
                    merged_current_set = True
                    break
            
            if not merged_current_set:
                merged.append(current_set)  # Add the current set to the merged list if it wasn't merged

        # Step 3: Update self.sets to hold the final merged sets
        self.sets = merged


  
    def print_active_sets(self):
        print ('Active Sets:', end= ' ')
        for set in enumerate(self.sets):
            print('{', end=' ')
            for value in set[1]:
                print(f"{self.deck.tiles[value]}", end=' ')
            print('}', end=' ')
        print('')
   
    def draw_tiles(self):
        for tile in self.deck.tiles:
            self.deck.tiles[tile].draw_tile(self.screen)  

