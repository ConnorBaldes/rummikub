import pygame
import os 
import re



# Tile class to represent each tile
class Tile:
    def __init__(self, id, num, color, image, x, y):
        self.id = id
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.num = num
        self.color = color
        self.rect.x = x
        self.rect.y = y
        self.original_pos = (x, y)  # Store original position in case of collision
    
    def __repr__(self):
        return f'{self.num}'
    
    def get_coordinates(self):
        return (self.rect.x, self.rect.y)
    
    def get_id(self):
        return (self.id)
    
    def draw_tile(self, screen):
        screen.blit(self.image, self.rect)

class Deck:
    def __init__(self):
        """
        Initialize the deck with all tiles and shuffle them.
        """
        self.tiles = self._initialize_tiles()

    def _initialize_tiles(self):
        """
        Create all tiles for the deck.
        :return: A list of Tile objects.
        """
        tile_files = self.get_tile_data('./tiles')

        tiles = {}
        for tile in tile_files:
                x_cord = 0
                y_cord = 900    
                tiles[tile[0]] = Tile(tile[0], tile[1], tile[2], tile[3], x_cord , y_cord)
                x_cord += 185

        return tiles

    def get_tile(self, id):

        return 

    def get_tile_data(self, folder_path):
        pattern = re.compile(r"tile_(\d+)_(\w+)\.png")
        tile_data = []
        tile_id = 0
        for filename in os.listdir(folder_path):
            match = pattern.match(filename)
            if match:
                number, color = match.groups()
                print(f'ID: {tile_id}, Number: {number}, Color: {color}, File Path: ./tiles/{filename}')
                tile_data.append((int(tile_id), int(number), color, f'./tiles/{filename}'))  # Convert number to int
                tile_id += 1

        return tile_data