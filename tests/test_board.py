import unittest
from rummikub.board import Board
from rummikub.tile import Tile

class TestBoard(unittest.TestCase):
    def setUp(self):
        """
        Set up a new board instance for each test.
        """
        self.board = Board()

    def test_add_valid_set(self):
        """
        Test adding a valid set to the board.
        """
        valid_set = [Tile(1, 'red'), Tile(2, 'red'), Tile(3, 'red')]
        self.board.add_set(valid_set)
        self.assertIn(valid_set, self.board.sets)

    def test_add_invalid_set(self):
        """
        Test adding an invalid set to the board (should raise ValueError).
        """
        invalid_set = [Tile(1, 'red'), Tile(1, 'red'), Tile(1, 'red')]  # Duplicates
        with self.assertRaises(ValueError):
            self.board.add_set(invalid_set)

    def test_is_valid_set(self):
        """
        Test the is_valid_set method with valid and invalid sets.
        """
        valid_set = [Tile(1, 'red'), Tile(2, 'red'), Tile(3, 'red')]
        invalid_set = [Tile(1, 'red'), Tile(1, 'red'), Tile(1, 'red')]

        self.assertTrue(self.board.is_valid_set(valid_set))
        self.assertFalse(self.board.is_valid_set(invalid_set))

    def test_board_representation(self):
        """
        Test the string representation of the board.
        """
        valid_set = [Tile(1, 'red'), Tile(2, 'red'), Tile(3, 'red')]
        self.board.add_set(valid_set)
        expected_repr = "Board([[Tile(1, red), Tile(2, red), Tile(3, red)]])"
        self.assertEqual(repr(self.board), expected_repr)

    def test_add_valid_set_with_joker_in_run(self):
        """
        Test adding a valid set with a joker used in a run.
        The joker should be placed correctly in a sequence.
        """
        valid_set_with_joker_in_run = [
            Tile(1, 'red'), Tile(None, None, is_joker=True), Tile(3, 'red')
        ]
        self.board.add_set(valid_set_with_joker_in_run)
        self.assertIn(valid_set_with_joker_in_run, self.board.sets)

    def test_add_valid_set_with_joker_in_group(self):
        """
        Test adding a valid set with a joker used in a group.
        The joker should be treated as a placeholder for a missing color.
        """
        valid_set_with_joker_in_group = [
            Tile(1, 'red'), Tile(1, 'blue'), Tile(None, None, is_joker=True)
        ]
        self.board.add_set(valid_set_with_joker_in_group)
        self.assertIn(valid_set_with_joker_in_group, self.board.sets)

    def test_add_invalid_set_with_joker_in_run(self):
        """
        Test adding an invalid set with a joker in a run (should raise ValueError).
        The joker should not break the sequence.
        """
        invalid_set_with_joker_in_run = [
            Tile(1, 'red'), Tile(None, None, is_joker=True), Tile(4, 'red')
        ]
        with self.assertRaises(ValueError):
            self.board.add_set(invalid_set_with_joker_in_run)

    def test_add_invalid_set_with_joker_in_group(self):
        """
        Test adding an invalid set with a joker in a group (should raise ValueError).
        The joker should not allow duplicates in the group.
        """
        invalid_set_with_joker_in_group = [
            Tile(1, 'red'), Tile(1, 'blue'), Tile(1, 'red'), Tile(None, None, is_joker=True)
        ]
        with self.assertRaises(ValueError):
            self.board.add_set(invalid_set_with_joker_in_group)


    def test_board_representation_with_joker(self):
        """
        Test the string representation of the board with jokers in a set.
        The joker should be represented as Tile(Joker).
        """
        valid_set_with_joker_in_run = [
            Tile(1, 'red'), Tile(None, None, is_joker=True), Tile(3, 'red')
        ]
        self.board.add_set(valid_set_with_joker_in_run)
        expected_repr = "Board([[Tile(1, red), Tile(Joker), Tile(3, red)]])"
        self.assertEqual(repr(self.board), expected_repr)

if __name__ == "__main__":
    unittest.main()
