import random

class Table:

    def __init__(self):
        #termcolor the library being used to color text does not have a 'black' color so 'green' is used instead
        self.tile_colors = ['red', 'green', 'blue', 'yellow']
        self.tile_values = list(range(1, 14))
        self.pool = []  # This will store the list of tiles
        self.sets = []  # This will store valid sets placed on the table
        self.manipulated_tiles = [] # Tiles a player has moved out of a set on the table

        # Call create_tiles function to populate the pool
        self.create_tiles()

    def create_tiles(self):
        tile_id = 1
        for color in self.tile_colors:
            for value in self.tile_values:
                self.pool.append((tile_id, value, color, False))
                tile_id += 1

        # Add joker tiles
        self.pool.append((105, 0, 'joker', True))
        self.pool.append((106, 0, 'joker', True))

    def take_tile_from_pool(self): 
        if not self.pool:
            print("Pool is empty.")
            return None
        else:
            random_tile = random.choice(self.pool)
            self.pool.remove(random_tile)
            return random_tile
        
    # During a given turn a player must be able to take a tile out of a valid set
    # and hold it while they manipulate other sets. move_tile_to_manipulated takes
    # the coordinates of a tile in 'sets', plucks that tile out of its set and places 
    # it in the holding list 'manipulated_tiles' 
    def move_tile_to_manipulated(self, set_index, tile_index):
        if set_index < 0 or set_index >= len(self.sets):
            print("Error: Invalid set index.")
            return
        if tile_index < 0 or tile_index >= len(self.sets[set_index]):
            print("Error: Invalid tile index in set.")
            return
        
        tile = self.sets[set_index].pop(tile_index)
        self.manipulated_tiles.append(tile)

    # Similiar to the move_tile_to_manipulated, place_tile_from_manipulated is 
    # tasked with taking a tile from the holding list 'manipulated_tiles' and 
    # placing it into a chosen position in the 'sets' list
    def place_tile_from_manipulated(self, set_index, tile_index, position):
        if set_index < 0 or set_index >= len(self.sets):
            print("Error: Invalid set index.")
            return
        if position < 0 or position > len(self.sets[set_index]):
            print("Error: Invalid position in set.")
            return
        if tile_index < 0 or tile_index >= len(self.manipulated_tiles):
            print("Error: Invalid tile index in manipulated tiles.")
            return

        tile_to_place = self.manipulated_tiles.pop(tile_index)
        self.sets[set_index].insert(position, tile_to_place)