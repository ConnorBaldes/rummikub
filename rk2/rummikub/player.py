from rummikub.tile import Tile
from rummikub.deck import Deck
from typing import List, Type, Dict, Iterator

class Player:
    def __init__(self, name: Type[str], initial_14: List[Tile]):

        self.name = name
        self.rack = self._build_rack(initial_14)
        self.initial_meld: bool = False

    def __repr__(self) -> Type[str]:
        return f'Player({self.name})'
    
    def __str__(self) -> Type[str]:
        return f'{self.name}'
    
    def __getitem__(self, id: int) -> Tile:
        return self.rack.get(str(id))
    
    def __setitem__(self, id: int, tile: Tile) -> None:
        self.rack[str(id)] = tile

    def __delitem__(self, id: int) -> Tile:
        return self.rack.pop(str(id))
    
    def __len__(self) -> int:
        return len(self.rack)
    
    def __iter__(self) -> Iterator[str]:
        return iter(self.rack)
    
    def __contains__(self, other: Tile) -> bool:
        if not isinstance(other, Tile):
            raise TypeError(f"Cannot compare Tile with {type(other).__name__}")
        return other in self.rack
    


    def _build_rack(self, tiles: List[Tile]) -> Dict: 
        rack = {}
        for tile in tiles:
            rack[tile.get_id()] = tile
        return rack

    def draw_tile(self, deck: Deck) -> None:     
        tile = deck.pick_tile()
        self.rack[tile.id] = tile

