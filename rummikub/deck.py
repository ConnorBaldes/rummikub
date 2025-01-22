import random
from rummikub.tile import Tile

class Deck:
    def __init__(self):
        """
        Initialize the deck with all tiles and shuffle them.
        """
        self.tiles = self._initialize_tiles()
        self.shuffle()

    def _initialize_tiles(self):
        """
        Create all tiles for the deck.
        :return: A list of Tile objects.
        """
        tiles = []
        colors = ['red', 'blue', 'orange', 'black']
        for color in colors:
            for number in range(1, 14):
                tiles.extend([Tile(number, color), Tile(number, color)]) # Two copies of each tile
        tiles.extend([Tile(None, None, True), Tile(None, None, True)])  # Jokers
        return tiles

    def shuffle(self):
        """
        Shuffle the deck of tiles.
        """
        random.shuffle(self.tiles)

    def draw_tile(self):
        """
        Draw a tile from the deck.
        :return: A Tile object if the deck is not empty, otherwise None.
        """
        return self.tiles.pop() if self.tiles else None

    def is_empty(self):
        """
        Check if the deck is empty.
        :return: True if the deck has no tiles, False otherwise.
        """
        return len(self.tiles) == 0
    
    def __repr__(self):
        """
        String representation of the deck for debugging.
        :return: A string describing the number of tiles in the deck.
        """
        return f"Deck({len(self.tiles)} tiles)"
