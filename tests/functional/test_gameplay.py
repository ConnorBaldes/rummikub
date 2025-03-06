import pytest
from unittest.mock import patch, MagicMock
import pygame
from rummikub.game import Game

class TestGameplay:
    """End-to-end tests for game functionality"""
    
    @pytest.fixture
    def game_fixture(self):
        """Create a game instance with mocked display"""
        with patch('pygame.display.set_mode'):
            with patch('pygame.image.load'):
                game = Game()
                
                # Mock the game_screen and its board
                game.game_screen = MagicMock()
                game.game_screen.board = MagicMock()
                
                # Create two players
                game.players = [MagicMock(), MagicMock()]
                game.players[0].name = "Player1"
                game.players[1].name = "Player2"
                game.players[0].tiles = {1: MagicMock(), 2: MagicMock()}
                game.players[1].tiles = {3: MagicMock(), 4: MagicMock()}
                
                game.current_turn = 0
                return game
    
    def test_next_turn(self, game_fixture):
        """Test the turn progression functionality"""
        game = game_fixture
        
        # Store the initial turn
        initial_turn = game.current_turn
        assert initial_turn == 0
        
        # Call next_turn and verify it advances
        with patch.object(game, 'change_screen'):  # Prevent actual screen change
            with patch.object(game, 'populate_rack'):  # Mock rack population
                with patch.object(game, 'save_positions'):  # Mock position saving
                    game.next_turn()
        
        # Verify turn advanced
        assert game.current_turn == 1
        assert game.statistics['turns_played'] == 1
        
        # Advance again to test looping back to player 1
        with patch.object(game, 'change_screen'):
            with patch.object(game, 'populate_rack'):
                with patch.object(game, 'save_positions'):
                    game.next_turn()
        
        assert game.current_turn == 0  # Back to first player
        assert game.statistics['turns_played'] == 2