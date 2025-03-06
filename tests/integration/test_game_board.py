import pytest
from unittest.mock import patch, MagicMock
from rummikub.game import Game
from rummikub.board import Board
from rummikub.player import Player
from rummikub.tile import Tile

class TestGameBoardIntegration:
    """Test integration between Game and Board components"""
    
    @pytest.fixture
    def setup_game_with_players(self, mock_surface):
        """Create a game with two players and some initial board state"""
        with patch('pygame.display.set_mode', return_value=mock_surface):
            with patch('pygame.image.load'):
                game = Game()
                
                # Mock deck to have controlled tiles
                game.deck.tiles = []  # Clear the randomized deck
                
                # Create players with known tiles
                player1 = Player(game, "Player1")
                player1.tiles = {}  # Clear random tiles
                
                player2 = Player(game, "Player2")
                player2.tiles = {}  # Clear random tiles
                
                game.players = [player1, player2]
                game.current_turn = 0
                
                return game
    
    def test_validate_turn_with_valid_set(self, setup_game_with_players, sample_tile_image):
        """Test validating a turn with a valid set on the board"""
        game = setup_game_with_players
        
        # Add tiles to board forming a valid group
        with patch('pygame.image.load', return_value=sample_tile_image):
            tiles = [
                Tile(1, 8, "red", "path/to/image.png"),
                Tile(2, 8, "blue", "path/to/image.png"),
                Tile(3, 8, "black", "path/to/image.png")
            ]
        
        # Mock game_screen and board
        game.game_screen = MagicMock()
        game.game_screen.board = Board(game)
        
        # Add tiles to the board
        for tile in tiles:
            game.game_screen.board.add_tile(tile)
        
        # Mock the initial meld check to return True
        with patch.object(game, 'check_initial_meld', return_value=True):
            # Test that validate_turn returns True with valid sets
            assert game.validate_turn() is True
            
            # Verify statistics tracking
            assert game.statistics['invalid_moves'] == 0