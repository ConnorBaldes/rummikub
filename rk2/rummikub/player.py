from rummikub.tile import Tile
from rummikub.deck import Deck
from typing import List, Type, Dict, Iterator

class Player:
    def __init__(self, game, name: Type[str]):

        self.game = game
        self.name = name
        self.tiles: Dict = self._build_rack()
        self.initial_meld: bool = False

    def _build_rack(self) -> Dict: 
        tiles = {}
        for _ in range(14):
            new_tile = self.game.deck.pick_tile()
            tiles[new_tile.get_id()] = new_tile
        return tiles

    def draw_tile(self) -> None:     
        new_tile = self.game.deck.pick_tile()
        self.tiles[new_tile.get_id()] = new_tile

    def add_tile(self, tile) -> None:
        self.tiles[tile.id] = tile

    def remove_tile(self, tile_id):
        return self.tiles.pop(tile_id, None)
    
    def draw(self, screen) -> None:
        for tile in self.tiles.values():
            tile.draw(screen)
