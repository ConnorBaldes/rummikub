from rummikub.tile import Tile
from typing import Type, List, Tuple
import re
import os

class Deck:

    def __init__(self, tile_folder: Type[str]):

        self.tile_folder = tile_folder
        self.tiles: List[Tile] = (self._shuffle(self._initialize_tiles()))


    def __len__(self) -> int:
        return len(self.tiles)
    
    def __bool__(self) -> bool:
        return bool(len(self.tiles))


    def __lt__(self, other) -> bool:
        
        if not isinstance(other, int):
            raise TypeError(f"Cannot compare Deck length with {type(other).__name__}")    
        return len(self.tiles) < other

    def __le__(self, other) -> bool:
        
        if not isinstance(other, int):
            raise TypeError(f"Cannot compare Deck length with {type(other).__name__}")   
        return len(self.tiles) <= other
    
    def __gt__(self, other) -> bool:
        if not isinstance(other, int):
            raise TypeError(f"Cannot compare Deck length with {type(other).__name__}")     
        return len(self.tiles) > other
    
    def __ge__(self, other) -> bool:
        if not isinstance(other, int):
            raise TypeError(f"Cannot compare Deck length with {type(other).__name__}")   
        return len(self.tiles) >= other
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, int):
            raise TypeError(f"Cannot compare Deck length with {type(other).__name__}")   
        return len(self.tiles) == other    

    def __ne__(self, other) -> bool:
        if not isinstance(other, int):
            raise TypeError(f"Cannot compare Deck length with {type(other).__name__}")   
        return len(self.tiles) != other
    

    def _get_tile_images(self) -> List[Tuple[int, Type[str], Type[str]]]:
        pattern = re.compile(r"tile_(\d+)_(\w+)\.png")
        tile_data = []
        tile_id = 0

        for filename in os.listdir(self.tile_folder):
            match = pattern.match(filename)
            if match:
                number, color = match.groups()
                tile_data.append((int(tile_id), int(number), color, f'{self.tile_folder}/{filename}'))
                tile_id += 1
        return tile_data

    def _initialize_tiles(self) -> List[Tile]:
        tile_files = self._get_tile_images()
        tiles = []

        for tile in tile_files:
                tiles.append(Tile(tile[0], tile[1], tile[2], tile[3]))
        return tiles
    # TO DO
    def _shuffle(self, tiles: List[Tile]) -> List[Tile]:
        return tiles
    
    def assign_tiles(self) -> List[Tile]:
        tiles = []
        for _ in range(14):
            tiles.append(self.tiles.pop())
        return tiles

    def pick_tile(self) -> Tile:
        return self.tiles.pop()




    

