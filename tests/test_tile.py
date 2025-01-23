import unittest
from rummikub.tile import Tile

class TestTile(unittest.TestCase):

    def test_tile_initialization(self):
        """
        Test that a normal tile is initialized correctly
        :param: tile number(5), tile color(red)
        """ 
        tile = Tile(5, 'red')
        self.assertEqual(tile.number, 5)
        self.assertEqual(tile.color, 'red')
        self.assertFalse(tile.is_joker)
 
    def test_joker_initialization(self):
        """
        Test that a joker tile is initialized correctly
        :param: tile number(None), tile color(None), is_joker(True)
        """
        joker = Tile(None, None, is_joker=True)
        self.assertEqual(joker.number, None)
        self.assertEqual(joker.color, None)
        self.assertTrue(joker.is_joker)

    
    

    def test_invalid_tile_color(self):
        """
        Test that tile.is_valid recognizes a tile with an invalid color
        :param: tile number(12), tile color(purple)
        """ 
        invalid_tile = Tile(12, 'purple')
        self.assertFalse(invalid_tile.is_valid())

    def test_invalid_tile_number(self):
        """
        Test that tile.is_valid recognizes a tile with an invalid number
        :param: tile number(15), tile color(red)
        """ 
        invalid_tile = Tile(12, 'purple')
        self.assertFalse(invalid_tile.is_valid())

    def test_invalid_joker_number(self):
        """
        Test that tile.is_valid recognizes a joker with an invalid number
        :param: tile number(10), tile color(None), is_joker(True)
        """ 
        invalid_tile = Tile(10, None, is_joker=True)
        self.assertFalse(invalid_tile.is_valid())

    def test_invalid_joker_color(self):
        """
        Test that tile.is_valid recognizes a joker with an invalid color
        :param: tile number(None), tile color(blue), is_joker(True)
        """ 
        invalid_tile = Tile(None, 'blue', is_joker=True)
        self.assertFalse(invalid_tile.is_valid())




    def test_tile_equality(self):
        """
        Test that tile.__eq__ recognizes that two tiles are equal
        :param: tile1 number(5), tile color(blue)
                tile2 number(5), tile color(blue)
        """ 
        tile1 = Tile(5, 'blue')
        tile2 = Tile(5, 'blue')
        self.assertEqual(tile1, tile2)

    def test_tile_inequality(self):
        """
        Test that tile.__eq__ recognizes that two tiles are not equal
        :param: tile1 number(6), tile color(blue)
                tile2 number(5), tile color(blue)
        """ 
        tile1 = Tile(6, 'blue')
        tile2 = Tile(5, 'blue')
        self.assertNotEqual(tile1, tile2)

