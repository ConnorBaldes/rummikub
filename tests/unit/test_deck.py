# tests/unit/test_deck.py
import pytest
import os
import random
from unittest.mock import MagicMock, patch, mock_open

from rummikub.deck import Deck
from rummikub.tile import Tile

class TestDeck:
    """Unit tests for the Deck class"""
    
    @pytest.fixture
    def mock_listdir(self):
        """Mock os.listdir to return a controlled set of tile filenames"""
        with patch('os.listdir') as mock_list:
            # Return a mixture of numbered tiles and jokers
            mock_list.return_value = [
                # Red tiles
                'tile_1_red.png',
                'tile_2_red.png',
                'tile_13_red.png',
                # Blue tiles
                'tile_1_blue.png',
                'tile_2_blue.png',
                'tile_13_blue.png',
                # Black tiles
                'tile_1_black.png',
                'tile_2_black.png',
                'tile_13_black.png',
                # Orange tiles
                'tile_1_orange.png',
                'tile_2_orange.png',
                'tile_13_orange.png',
                # Jokers
                'tile_joker_1.png',
                'tile_joker_2.png',
                # Non-matching files that should be ignored
                'background.png',
                'readme.txt'
            ]
            yield mock_list
    
    @pytest.fixture
    def mock_tile_class(self):
        """Mock the Tile class to avoid actual image loading"""
        with patch('rummikub.deck.Tile') as MockTile:
            # Configure the mock to return unique instances
            MockTile.side_effect = lambda id, number, color, path, is_joker=False: MagicMock(
                id=id,
                number=number,
                color=color,
                is_joker=is_joker,
                spec=Tile
            )
            yield MockTile
    
    @pytest.fixture
    def mock_shuffle(self):
        """Mock random.shuffle to avoid randomness in tests"""
        with patch('random.shuffle') as mock_shuffle:
            # Make shuffle just return the same list to make tests predictable
            mock_shuffle.side_effect = lambda x: x
            yield mock_shuffle
    
    def test_initialization(self, mock_listdir, mock_tile_class, mock_shuffle):
        """Test deck initialization with mock tiles"""
        deck = Deck("rummikub/assets/tiles_2")
        
        # Verify os.listdir was called with the correct folder
        mock_listdir.assert_called_once_with("rummikub/assets/tiles_2")
        
        # Calculate expected tile count: 12 numbered tiles * 2 (duplicates) + 2 jokers = 26
        expected_tile_count = 12 * 2 + 2
        
        # Verify deck size
        assert len(deck) == expected_tile_count
        
        # Verify shuffle was called
        mock_shuffle.assert_called_once()
        
        # Verify Tile creation
        assert mock_tile_class.call_count == expected_tile_count
    
    def test_get_tile_images(self, mock_listdir):
        """Test _get_tile_images method with mock directory listing"""
        deck = Deck("rummikub/assets/tiles_2")
        
        # Call the method directly for testing
        tile_data = deck._get_tile_images()
        
        # Calculate expected counts
        expected_numbered_tiles = 12 * 2  # 12 numbered tiles * 2 (duplicates)
        expected_joker_tiles = 2
        expected_total = expected_numbered_tiles + expected_joker_tiles
        
        # Verify the returned data length
        assert len(tile_data) == expected_total
        
        # Verify structure and content of some entries
        for id, number, color, path, is_joker in tile_data:
            # Verify ID is an integer
            assert isinstance(id, int)
            
            # Verify number is an integer
            assert isinstance(number, int)
            
            # Verify is_joker flag is a boolean
            assert isinstance(is_joker, bool)
            
            # Verify path format
            assert path.startswith("rummikub/assets/tiles_2")
            
            if is_joker:
                # Jokers should have number 0 and color "joker"
                assert number == 0
                assert color == "joker"
            else:
                # Regular tiles should have a number 1-13
                assert 1 <= number <= 13
                assert color in ["red", "blue", "black", "orange"]
    
    def test_initialize_tiles(self, mock_listdir, mock_tile_class):
        """Test _initialize_tiles method"""
        deck = Deck("rummikub/assets/tiles_2")
        
        # Bypass normal initialization to test _initialize_tiles directly
        with patch.object(deck, '_get_tile_images') as mock_get_images:
            # Set up mock tile data
            mock_get_images.return_value = [
                (0, 1, "red", "rummikub/assets/tiles_2/tile_1_red.png", False),
                (1, 2, "blue", "rummikub/assets/tiles_2/tile_2_orange.png", False),
                (2, 0, "joker", "rummikub/assets/tiles_2/tile_joker_1.png", True)
            ]
            
            # Call method
            tiles = deck._initialize_tiles()
            
            # Verify tiles were created with correct parameters
            assert len(tiles) == 3
            
            # Reset mock to clear previous calls from initialization
            mock_tile_class.reset_mock()
            
            # Verify Tile constructor was called with correct arguments
            expected_calls = [
                ((0, 1, "red", "path/to/tile1.png"), {"is_joker": False}),
                ((1, 2, "blue", "path/to/tile2.png"), {"is_joker": False}),
                ((2, 0, "joker", "path/to/joker.png"), {"is_joker": True})
            ]
            
            # Check each call
            assert mock_tile_class.call_count == 3
            for i, (args, kwargs) in enumerate(mock_tile_class.call_args_list):
                exp_args, exp_kwargs = expected_calls[i]
                assert args == exp_args
                assert kwargs == exp_kwargs
    
    def test_shuffle(self):
        """Test the _shuffle method"""
        # Create a list of mock tiles
        mock_tiles = [MagicMock(spec=Tile) for _ in range(5)]
        
        with patch('random.shuffle') as mock_shuffle:
            deck = Deck("rummikub/assets/tiles_2")
            
            # Call shuffle directly
            shuffled = deck._shuffle(mock_tiles)
            
            # Verify random.shuffle was called with the tiles
            mock_shuffle.assert_called_once_with(mock_tiles)
            
            # Verify shuffled list is returned
            assert shuffled is mock_tiles
    
    def test_pick_tile(self, mock_listdir, mock_tile_class):
        """Test picking a tile from the deck"""
        deck = Deck("rummikub/assets/tiles_2")
        
        # Get initial deck size
        initial_size = len(deck)
        
        # Pick a tile
        tile = deck.pick_tile()
        
        # Verify tile is returned
        assert tile is not None
        assert isinstance(tile, MagicMock)  # Our mock tile
        
        # Verify deck size decreased
        assert len(deck) == initial_size - 1
    
    def test_pick_all_tiles(self, mock_listdir, mock_tile_class):
        """Test picking all tiles from the deck"""
        deck = Deck("rummikub/assets/tiles_2")
        
        # Get initial deck size
        initial_size = len(deck)
        
        # Pick all tiles
        tiles = [deck.pick_tile() for _ in range(initial_size)]
        
        # Verify all tiles were picked
        assert len(tiles) == initial_size
        assert len(deck) == 0
        
        # Verify picking from empty deck raises IndexError
        with pytest.raises(IndexError):
            deck.pick_tile()
    
    def test_len(self, mock_listdir, mock_tile_class):
        """Test the __len__ method"""
        deck = Deck("rummikub/assets/tiles_2")
        
        # Initial length
        initial_length = len(deck)
        
        # Pick some tiles
        for _ in range(3):
            deck.pick_tile()
        
        # Verify length decreased
        assert len(deck) == initial_length - 3
        
        # Pick the rest
        for _ in range(len(deck)):
            deck.pick_tile()
        
        # Verify empty deck has length 0
        assert len(deck) == 0