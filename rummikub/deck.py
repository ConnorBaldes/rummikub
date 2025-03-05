from rummikub.tile import Tile
from typing import Type, List, Tuple
import re
import os
import random

class Deck:

    def __init__(self, tile_folder: Type[str]):
        self.tile_folder = tile_folder
        self.tiles: List[Tile] = (self._shuffle(self._initialize_tiles()))

    def __len__(self) -> int:
        return len(self.tiles)

    def _get_tile_images(self) -> List[Tuple[int, Type[str], Type[str]]]:
        # Pattern for regular numbered tiles
        number_pattern = re.compile(r"tile_(\d+)_(\w+)\.png")
        # Pattern for joker tiles
        joker_pattern = re.compile(r"tile_joker_(\d+)\.png")
        
        tile_data = []
        tile_id = 0

        for filename in os.listdir(self.tile_folder):
            # Check for regular numbered tiles
            match = number_pattern.match(filename)
            if match:
                number, color = match.groups()
                tile_data.append((int(tile_id), int(number), color, f'{self.tile_folder}/{filename}', False))
                tile_data.append((int(tile_id + 1), int(number), color, f'{self.tile_folder}/{filename}', False))
                tile_id += 2
                continue
            
            # Check for joker tiles
            joker_match = joker_pattern.match(filename)
            if joker_match:
                # For jokers, we'll use 0 as the number and "joker" as the color
                tile_data.append((int(tile_id), 0, "joker", f'{self.tile_folder}/{filename}', True))
                tile_id += 1
                
        return tile_data

    def _initialize_tiles(self) -> List[Tile]:
        tile_files = self._get_tile_images()
        tiles = []

        for tile in tile_files:
            # Unpack the tile data (now includes is_joker flag)
            tile_id, number, color, image_path, is_joker = tile
            tiles.append(Tile(tile_id, number, color, image_path, is_joker=is_joker))
        return tiles
    
    def _shuffle(self, tiles: List[Tile]) -> List[Tile]:
        """Shuffles the deck of tiles randomly."""
        random.shuffle(tiles)
        return tiles

    def pick_tile(self) -> Tile:
        return self.tiles.pop()




    

