import unittest
from rummikub.player import Player
from rummikub.deck import Deck
from rummikub.tile import Tile

class TestPlayer(unittest.TestCase):
    def setUp(self):
        """
        Set up a new player and deck instance for each test.
        """
        self.player = Player("Alice")
        self.deck = Deck()

    def test_player_initialization(self):
        """
        Test that the player is initialized correctly.
        """
        self.assertEqual(self.player.name, "Alice")
        self.assertEqual(len(self.player.hand), 0)

    def test_draw_tile(self):
        """
        Test drawing a tile from the deck.
        """
        self.player.draw_tile(self.deck)
        self.assertEqual(len(self.player.hand), 1)
        self.assertEqual(len(self.deck.tiles), 105)

    def test_play_valid_tiles(self):
        """
        Test playing valid tiles from the player's hand.
        """
        # Add tiles to the player's hand
        tile1 = Tile(5, 'red')
        tile2 = Tile(6, 'red')
        self.player.hand.extend([tile1, tile2])

        # Play one tile
        self.player.play_tiles([tile1])
        self.assertNotIn(tile1, self.player.hand)
        self.assertIn(tile2, self.player.hand)

    def test_play_invalid_tiles(self):
        """
        Test playing tiles not in the player's hand (should raise ValueError).
        """
        tile1 = Tile(5, 'red')  # Not in hand
        with self.assertRaises(ValueError):
            self.player.play_tiles([tile1])

    def test_player_representation(self):
        """
        Test the string representation of the player.
        """
        tile1 = Tile(5, 'red')
        self.player.hand.append(tile1)
        expected_repr = "Player(Alice, Hand: [Tile(5, red)])"
        self.assertEqual(repr(self.player), expected_repr)

if __name__ == "__main__":
    unittest.main()
