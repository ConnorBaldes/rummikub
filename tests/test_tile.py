import unittest
from rummikub.tile import Tile

class TestTile(unittest.TestCase):

    def test_tile_initialization(self):
        tile = Tile(5, 'red')
        self.assertEqual(tile.number, 5)
        self.assertEqual(tile.color, 'red')
        self.assertFalse(tile.is_joker)
        
    def test_joker_tile(self):
        joker = Tile(None, None, is_joker=True)
        self.assertTrue(joker.is_joker)

    def test_invalid_tile(self):
        invalid_tile = Tile(15, 'purple')
        self.assertFalse(invalid_tile.is_valid())