import unittest
from rummikub.deck import Deck

class TestDeck(unittest.TestCase):
    
    def test_deck_initialization(self):
        deck = Deck()
        self.assertEqual(len(deck.tiles), 106)

    def test_deck_draw(self):
        deck = Deck()
        tile = deck.draw_tile()
        self.assertIsNotNone(tile)
        self.assertEqual(len(deck.tiles), 105)

    def test_deck_shuffle(self):
        deck = Deck()
        original_order = deck.tiles[:]
        deck.shuffle()
        self.assertNotEqual(deck.tiles, original_order)
