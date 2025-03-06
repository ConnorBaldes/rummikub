# In tests/conftest.py
import os
import sys
import pytest
import pygame
import numpy as np
from unittest.mock import MagicMock, patch

# Add the project root directory to Python's module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock pygame initialization to avoid display issues during testing
@pytest.fixture(scope="session", autouse=True)
def pygame_setup():
    """Initialize pygame without a display for all tests"""
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    pygame.init()
    yield
    pygame.quit()

@pytest.fixture
def mock_surface():
    """Create a mock pygame surface for testing"""
    surface = MagicMock()
    surface.get_width.return_value = 3400
    surface.get_height.return_value = 2500
    surface.get_rect.return_value = pygame.Rect(0, 0, 3400, 2500)
    return surface

@pytest.fixture
def sample_tile_image():
    """Create a simple surface to use as a tile image"""
    return pygame.Surface((130, 200))

@pytest.fixture
def mock_game():
    """Create a mock game object"""
    from rummikub.game import Game
    with patch('pygame.display.set_mode'):
        game = MagicMock(spec=Game)
        game.screen = mock_surface()
        return game

@pytest.fixture
def sample_deck():
    """Create a sample deck with a few tiles for testing"""
    from rummikub.deck import Deck
    with patch('os.listdir') as mock_listdir:
        # Mock file listing to return a controlled set of tile images
        mock_listdir.return_value = [
            'tile_1_red.png', 'tile_2_blue.png', 'tile_3_black.png',
            'tile_4_orange.png', 'tile_joker_1.png'
        ]
        
        # Mock image loading
        with patch('pygame.image.load'):
            return Deck("./rummikub/assets/tiles_2")

@pytest.fixture
def empty_board(mock_game):
    """Create an empty board for testing"""
    from rummikub.board import Board
    return Board(mock_game)