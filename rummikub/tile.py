class Tile:
    def __init__(self, number, color, is_joker=False):
        """
        Initialize a tile.
        :param number: Number on the tile (1-13) or None for jokers.
        :param color: Color of the tile (e.g., 'red', 'blue', 'orange', 'black').
        :param is_joker: True if this tile is a joker, otherwise False.
        """
        self.number = number
        self.color = color
        self.is_joker = is_joker

    def __repr__(self):
        """
        String representation of the tile for debugging.
        :return: A string describing the tile.
        """
        if self.is_joker:
            return "Tile(Joker)"
        return f"Tile({self.number}, {self.color})"
    
    def __eq__(self, other):
        """
        Equality comparison for tiles.
        :param other: Another Tile instance.
        :return: True if the tiles are identical, False otherwise.
        """
        return (
            isinstance(other, Tile)
            and self.number == other.number
            and self.color == other.color
            and self.is_joker == other.is_joker
        )   
    
    def __hash__(self):
        """Override hash function to use number and color."""
        return hash((self.number, self.color))

    def is_valid(self):
        """
        Check if the tile is valid.
        :return: True if the tile has valid attributes, False otherwise.
        """
        if self.is_joker:
            # Joker tiles must have color=None and number=None
            return self.color is None and self.number is None

        valid_numbers = list(range(1, 14))
        valid_colors = ['red', 'blue', 'orange', 'black']
        return self.number in valid_numbers and self.color in valid_colors