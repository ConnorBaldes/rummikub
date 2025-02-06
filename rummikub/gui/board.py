import pygame
from deck import Deck
from deck import Tile

class Board:
    def __init__(self):

        self.screen = pygame.display.set_mode((2400, 1800))
        self.deck = Deck()
        self.sets = []

    def set_title(self, title= "Rummikub"):
        pygame.display.set_caption(title)

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

