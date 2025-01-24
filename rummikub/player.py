from rummikub.tile import Tile
from rummikub.deck import Deck

class Player:
    def __init__(self, name):
        """
        Initialize a player.
        :param name: The player's name.
        """
        self.name = name
        self.hand = []
        self.initial_meld = False

    def draw_tile(self, deck) -> Tile:
        """
        Draw a tile from the deck and add it to the player's hand.
        :param deck: The Deck instance to draw from.
        : return: The tile object drawn from the deck(for game start)
        """
        tile = deck.draw_tile()
        if tile:
            self.hand.append(tile)
        return tile

    def play_tiles(self, tiles):
        """
        Remove tiles from the player's hand.
        :param tiles: A list of Tile objects to play.
        :raises ValueError: If any tile is not in the player's hand.
        """
        for tile in tiles:
            if tile not in self.hand:
                raise ValueError(f"Tile {tile} is not in the player's hand.")
            self.hand.remove(tile)

    def __repr__(self):
        """
        String representation of the player for debugging.
        :return: A string describing the player's name and hand.
        """
        return f"Player({self.name}, Hand: {self.hand}, Initial Meld: {self.initial_meld})"
