# tests/unit/test_game.py
import pytest
import pygame
from unittest.mock import MagicMock, patch, call

from rummikub.game import Game
from rummikub.player import Player
from rummikub.deck import Deck
from rummikub.tile import Tile
from rummikub.screens.game_screen import GameScreen
from rummikub.screens.menu import SetupMenu, TurnMenu

class TestGame:
    """Unit tests for the Game class"""
    
    @pytest.fixture
    def mock_pygame(self):
        """Mock pygame to avoid actual initialization"""
        with patch('pygame.init') as mock_init, \
             patch('pygame.display.set_mode') as mock_set_mode, \
             patch('pygame.display.set_caption') as mock_set_caption, \
             patch('pygame.time.Clock') as mock_clock:
                
            # Configure mocks
            mock_screen = MagicMock()
            mock_screen.get_width.return_value = 3400
            mock_set_mode.return_value = mock_screen
            
            mock_clock_instance = MagicMock()
            mock_clock.return_value = mock_clock_instance
            
            yield {
                'init': mock_init,
                'set_mode': mock_set_mode,
                'set_caption': mock_set_caption,
                'clock': mock_clock_instance,
                'screen': mock_screen
            }
    
    @pytest.fixture
    def mock_deck(self):
        """Mock Deck class"""
        with patch('rummikub.game.Deck') as MockDeck:
            # Configure mock deck
            mock_deck_instance = MagicMock(spec=Deck)
            mock_deck_instance.__len__.return_value = 50  # Default remaining tiles
            MockDeck.return_value = mock_deck_instance
            
            yield MockDeck, mock_deck_instance
    
    @pytest.fixture
    def mock_screens(self):
        """Mock screen classes with accurate Board implementation"""
        # Create a comprehensive Board mock based on the actual class
        mock_board = MagicMock()
        mock_board.game = None  # Will be set later
        mock_board.graph = MagicMock()
        mock_board.tiles = {}
        mock_board.added_tiles = []
        
        # Add methods from Board class
        mock_board.add_tile = MagicMock()
        mock_board.remove_tile = MagicMock()
        mock_board.draw = MagicMock()
        mock_board.is_valid_group = MagicMock(return_value=True)
        mock_board.is_valid_run = MagicMock(return_value=True)
        mock_board.update_sets = MagicMock()
        mock_board._assign_joker_run_values = MagicMock()
        mock_board.snap_tile = MagicMock()
        mock_board.validate_sets = MagicMock(return_value=True)
        mock_board.reset_board = MagicMock()
        mock_board.get_tile_positions = MagicMock(return_value={})
        
        # Additional attribute needed for initial meld tests
        mock_board.initial_meld_played = False
        mock_board.get_initial_meld_value = MagicMock(return_value=0)
        
        # Mock the screen classes
        with patch('rummikub.game.SetupMenu') as MockSetupMenu, \
            patch('rummikub.game.GameScreen') as MockGameScreen, \
            patch('rummikub.game.TurnMenu') as MockTurnMenu:
                
            # Configure mock screens
            mock_setup_menu = MagicMock()
            mock_setup_menu.draw = MagicMock()
            mock_setup_menu.update = MagicMock()
            mock_setup_menu.handle_events = MagicMock()
            
            # Create game_screen with board attribute
            mock_game_screen = MagicMock()
            mock_game_screen.render = MagicMock()
            mock_game_screen.draw = MagicMock()
            mock_game_screen.update = MagicMock()
            mock_game_screen.handle_events = MagicMock()
            mock_game_screen.board = mock_board  # Attach our board mock
            
            mock_turn_menu = MagicMock()
            mock_turn_menu.draw = MagicMock()
            mock_turn_menu.update = MagicMock()
            mock_turn_menu.handle_events = MagicMock()
            
            MockSetupMenu.return_value = mock_setup_menu
            MockGameScreen.return_value = mock_game_screen
            MockTurnMenu.return_value = mock_turn_menu
            
            yield {
                'SetupMenu': MockSetupMenu,
                'GameScreen': MockGameScreen,
                'TurnMenu': MockTurnMenu,
                'setup_menu': mock_setup_menu,
                'game_screen': mock_game_screen,
                'turn_menu': mock_turn_menu,
                'board': mock_board  # Include board in returned dict
            }
    
    @pytest.fixture
    def game(self, mock_pygame, mock_deck, mock_screens):
        """Create a game instance with mocked dependencies"""
        _, mock_deck_instance = mock_deck
        
        # Create the game
        game = Game()
        
        # Verify initialization happened correctly
        assert game.deck == mock_deck_instance
        assert game.screen == mock_pygame['screen']
        assert game.clock == mock_pygame['clock']
        assert game.current_screen == mock_screens['setup_menu']
        
        # Reset mocks to clear initialization calls
        for mock in mock_pygame.values():
            if hasattr(mock, 'reset_mock'):
                mock.reset_mock()
        
        return game
    
    @pytest.fixture
    def mock_players(self, game):
        """Create mock players for testing"""
        # Create mock players
        player1 = MagicMock(spec=Player)
        player1.name = "Player 1"
        player1.initial_meld = False
        player1.tiles = {}
        
        player2 = MagicMock(spec=Player)
        player2.name = "Player 2"
        player2.initial_meld = True  # Already met initial meld
        player2.tiles = {}
        
        # Add to game
        game.players = [player1, player2]
        game.current_turn = 0  # Start with player 1
        
        return [player1, player2]
    
    @pytest.fixture
    def mock_tiles(self):
        """Create configurable mock tiles"""
        def _create_tile(tile_id, number, color, is_joker=False, x=0, y=0):
            tile = MagicMock(spec=Tile)
            tile.id = tile_id
            tile.number = number
            tile.get_number.return_value = number
            tile.color = color
            tile.is_joker = is_joker
            tile.image = MagicMock()
            tile.image.get_width.return_value = 140
            tile.image.get_height.return_value = 200
            tile.rect = MagicMock()
            tile.rect.width = 140
            tile.rect.height = 200
            tile.rect.x = x
            tile.rect.y = y
            tile.set_coordinates = MagicMock()
            tile.save_turn_start_position = MagicMock()
            tile.save_pre_drag_pos = MagicMock()
            return tile
        return _create_tile
    
    def test_initialization(self, mock_pygame, mock_deck, mock_screens):
        """Test game initialization"""
        MockDeck, _ = mock_deck
        
        # Create game
        game = Game()
        
        # Verify pygame initialization
        mock_pygame['init'].assert_called_once()
        mock_pygame['set_mode'].assert_called_once_with((3400, 2500))
        mock_pygame['set_caption'].assert_called_once_with("Rummikub")
        
        # Verify deck initialization
        MockDeck.assert_called_once_with("./rummikub/assets/tiles_2")
        
        # Verify screen initialization
        mock_screens['SetupMenu'].assert_called_once_with(game)
        mock_screens['GameScreen'].assert_called_once_with(game)
        
        # Verify initial game state
        assert game.running == True
        assert game.current_turn == 0
        assert game.players == []
        assert game.game_over == False
        assert game.winner is None
        
        # Verify statistics initialization
        assert game.statistics == {
            'turns_played': 0,
            'tiles_drawn': 0,
            'valid_sets_formed': 0,
            'invalid_moves': 0
        }
        
        # Verify initial screen
        assert game.current_screen == mock_screens['setup_menu']
    
    def test_change_screen(self, game, mock_screens):
        """Test changing the active screen"""
        # Change to game screen
        game.change_screen(mock_screens['game_screen'])
        
        # Verify screen change
        assert game.current_screen == mock_screens['game_screen']
        
        # Change to turn menu screen
        game.change_screen(mock_screens['turn_menu'])
        
        # Verify screen change
        assert game.current_screen == mock_screens['turn_menu']
    
    def test_handle_events(self, game):
        """Test event handling"""
        # Mock pygame.event.get
        mock_events = [MagicMock(), MagicMock()]
        with patch('pygame.event.get', return_value=mock_events) as mock_get:
            # Set a quit event
            mock_events[0].type = pygame.QUIT
            
            # Handle events
            game.handle_events()
            
            # Verify pygame.event.get was called
            mock_get.assert_called_once()
            
            # Verify game.running was set to False due to quit event
            assert game.running == False
            
            # Verify current_screen.handle_events was called with events
            game.current_screen.handle_events.assert_called_once_with(mock_events)
    
    def test_update(self, game):
        """Test game update method"""
        # Call update
        game.update()
        
        # Verify current_screen.update was called
        game.current_screen.update.assert_called_once()
    
    def test_render_non_game_screen(self, game, mock_screens):
        """Test rendering a non-game screen"""
        # Ensure current screen is not game_screen
        game.current_screen = mock_screens['setup_menu']
        
        # Mock pygame.display.flip
        with patch('pygame.display.flip') as mock_flip:
            # Call render
            game.render()
            
            # Verify screen.draw was called with the game screen
            game.current_screen.draw.assert_called_once_with(game.screen)
            
            # Verify display.flip was called
            mock_flip.assert_called_once()
    
    def test_render_game_screen(self, game, mock_screens):
        """Test rendering the game screen"""
        # Set current screen to game_screen
        game.current_screen = mock_screens['game_screen']
        
        # Call render
        game.render()
        
        # Verify game_screen.render was called instead of draw
        game.current_screen.render.assert_called_once()
        game.current_screen.draw.assert_not_called()
    
    def test_populate_rack_empty(self, game, mock_players):
        """Test populating rack with no tiles"""
        # Ensure player has no tiles
        game.players[0].tiles = {}
        
        # Make a copy of the empty tiles to compare later
        original_tiles = game.players[0].tiles.copy()
        
        # Call populate_rack
        game.populate_rack()
        
        # Verify nothing changed (empty tiles dictionary remained empty)
        assert game.players[0].tiles == original_tiles
        # Or directly assert that tiles is still an empty dictionary
        assert game.players[0].tiles == {}
    
    def test_populate_rack_with_tiles(self, game, mock_players, mock_tiles):
        """Test populating rack with tiles"""
        # Create sample tiles
        tile1 = mock_tiles(1, 8, "red")
        tile2 = mock_tiles(2, 9, "blue")
        tile3 = mock_tiles(3, 10, "black")
        
        # Add tiles to player
        game.players[0].tiles = {1: tile1, 2: tile2, 3: tile3}
        
        # Call populate_rack
        game.populate_rack()
        
        # Verify coordinates were set for each tile
        assert tile1.set_coordinates.called
        assert tile2.set_coordinates.called
        assert tile3.set_coordinates.called
        
        # Verify tiles are arranged in a grid with appropriate spacing
        calls = [call.args for call in tile1.set_coordinates.call_args_list + 
                             tile2.set_coordinates.call_args_list + 
                             tile3.set_coordinates.call_args_list]
        
        # Check that each tile has a different position
        positions = set()
        for args in calls:
            x, y = args
            positions.add((x, y))
        
        assert len(positions) == 3  # All tiles should have unique positions
    
    def test_save_positions(self, game, mock_screens):
        """Test saving tile positions"""
        # Configure the mock to return some tile positions
        positions = {1: (100, 200), 2: (300, 400)}
        mock_screens['board'].get_tile_positions.return_value = positions
        
        # Set the game's current screen to the game screen
        game.current_screen = mock_screens['game_screen']
        
        # Call the method being tested
        game.save_positions()
        
        # Verify the appropriate methods were called
        mock_screens['board'].get_tile_positions.assert_called_once()
    
    def test_next_turn(self, game, mock_players, mock_screens):
        """Test advancing to the next player's turn"""
        # Mock TurnMenu constructor
        # Mock populate_rack and save_positions
        with patch.object(game, 'populate_rack') as mock_populate, \
             patch.object(game, 'save_positions') as mock_save, \
             patch.object(game, 'change_screen') as mock_change_screen, \
             patch('builtins.print') as mock_print:
            
            # Initial state
            assert game.current_turn == 0
            assert game.statistics['turns_played'] == 0
            
            # Advance to next turn
            game.next_turn()
            
            # Verify player index advanced
            assert game.current_turn == 1
            
            # Verify statistics were updated
            assert game.statistics['turns_played'] == 1
            
            # Verify methods were called
            mock_populate.assert_called_once()
            mock_save.assert_called_once()
            
            # Verify new TurnMenu was created with proper messages
            turn_msg = f"{game.players[1].name}"
            stats_msg = (f"Game Statistics: 1 turns played, "
                         f"0 tiles drawn, "
                         f"50 tiles remaining in deck")
            
            mock_screens['TurnMenu'].assert_called_once_with(game, turn_msg, stats_msg)
            
            # Verify screen was changed
            mock_change_screen.assert_called_once()
            
            # Verify player turn was printed
            mock_print.assert_called_once_with("Player 2's turn")
            
            # Advance again to wrap around to first player
            game.next_turn()
            
            # Verify wrapped back to first player
            assert game.current_turn == 0
            assert game.statistics['turns_played'] == 2
    
    def test_validate_turn_no_tiles_played(self, game, mock_screens):
        """Test validating turn when no tiles were played"""
        # Configure board with no added tiles
        game.game_screen.board.added_tiles = []
        
        # Mock print
        with patch('builtins.print') as mock_print:
            # Validate turn
            result = game.validate_turn()
            
            # Verify result is False
            assert result == False
            
            # Verify invalid moves count increased
            assert game.statistics['invalid_moves'] == 1
            
            # Verify message was printed
            mock_print.assert_called_once_with('No tiles played.')
    
    def test_validate_turn_valid_move(self, game, mock_screens):
        """Test validating turn with valid moves"""
        # Configure board with added tiles
        game.game_screen.board.added_tiles = [1, 2, 3]
        
        # Mock methods to return success
        with patch.object(game, 'check_initial_meld', return_value=True) as mock_check, \
             patch.object(game.game_screen.board, 'validate_sets', return_value=True) as mock_validate:
            
            # Validate turn
            result = game.validate_turn()
            
            # Verify result is True
            assert result == True
            
            # Verify methods were called
            mock_check.assert_called_once()
            mock_validate.assert_called_once()
            
            # Verify invalid moves count did not increase
            assert game.statistics['invalid_moves'] == 0
    
    def test_validate_turn_invalid_initial_meld(self, game, mock_screens):
        """Test validating turn with invalid initial meld"""
        # Configure board with added tiles
        game.game_screen.board.added_tiles = [1, 2, 3]
        
        # Mock methods to return failure on initial meld
        with patch.object(game, 'check_initial_meld', return_value=False) as mock_check:
            
            # Validate turn
            result = game.validate_turn()
            
            # Verify result is False
            assert result == False
            
            # Verify check_initial_meld was called
            mock_check.assert_called_once()
            
            # Verify validate_sets was not called (early return)
            game.game_screen.board.validate_sets.assert_not_called()
            
            # Verify invalid moves count increased
            assert game.statistics['invalid_moves'] == 1
    
    def test_check_initial_meld_already_met(self, game, mock_players):
        """Test checking initial meld that was already met"""
        # Set player to one who already met initial meld
        game.current_turn = 1  # Player 2
        
        # Mock print
        with patch('builtins.print') as mock_print:
            # Check initial meld
            result = game.check_initial_meld()
            
            # Verify result is True
            assert result == True
            
            # Verify message was printed
            mock_print.assert_called_once_with("Initial meld already met in a previous turn.")
    
    def test_check_initial_meld_sufficient_value(self, game, mock_screens):
        """Test checking if initial meld has sufficient value (>=30)"""
        # Configure the mock to return a sufficient value
        mock_screens['board'].get_initial_meld_value.return_value = 30
        
        # Set the game's current screen to the game screen
        game.current_screen = mock_screens['game_screen']
        
        # Call the method being tested
        result = game.check_initial_meld()
        
        # Assert the expected result
        assert result is True
        mock_screens['board'].get_initial_meld_value.assert_called_once()

    def test_check_initial_meld_insufficient_value(self, game, mock_screens):
        """Test checking if initial meld has insufficient value (<30)"""
        # Configure the mock to return an insufficient value
        mock_screens['board'].get_initial_meld_value.return_value = 29
        
        # Set the game's current screen to the game screen
        game.current_screen = mock_screens['game_screen']
        
        # Call the method being tested
        result = game.check_initial_meld()
        
        # Assert the expected result
        assert result is False
        mock_screens['board'].get_initial_meld_value.assert_called_once()
        
        def test_check_for_win_no_winner(self, game, mock_players, mock_tiles):
            """Test checking for win when player still has tiles"""
            # Ensure player has tiles
            tile1 = mock_tiles(1, 5, "red")
            game.players[0].tiles = {1: tile1}
            
            # Mock print
            with patch('builtins.print') as mock_print:
                # Check for win
                result = game.check_for_win()
                
                # Verify result is False
                assert result == False
                
                # Verify game state was not changed
                assert game.game_over == False
                assert game.winner is None
                
                # Verify message was printed
                mock_print.assert_called_once_with("Player Player 1 still has 1 tiles left.")
    
    def test_check_for_win_winner(self, game, mock_players, mock_screens):
        """Test checking for win when player has no tiles"""
        # Ensure player has no tiles
        game.players[0].tiles = {}
        
        # Mock SetupMenu and print
        with patch('builtins.print') as mock_print, \
             patch.object(game, 'change_screen') as mock_change_screen:
            
            # Check for win
            result = game.check_for_win()
            
            # Verify result is True
            assert result == True
            
            # Verify game state was updated
            assert game.game_over == True
            assert game.winner == "Player 1"
            
            # Verify message was printed
            mock_print.assert_called_once_with("Player Player 1 has no tiles left and wins the game!")
            
            # Verify new SetupMenu was created with win message
            win_message = "Player 1 wins the game with 0 turns played!"
            mock_screens['SetupMenu'].assert_called_with(game, win_message)
            
            # Verify screen was changed
            mock_change_screen.assert_called_once()
    
    def test_run(self, game):
        """Test game run loop"""
        # Set up game to run for 3 loops then exit
        game.running = True
        
        def side_effect_handler():
            # Decrement the counter each time handle_events is called
            game._counter -= 1
            if game._counter <= 0:
                game.running = False
        
        # Set up mocks and counter
        with patch.object(game, 'handle_events', side_effect=side_effect_handler) as mock_handle, \
             patch.object(game, 'update') as mock_update, \
             patch.object(game, 'render') as mock_render, \
             patch('pygame.quit') as mock_quit:
            
            # Set counter and run game
            game._counter = 3
            game.run()
            
            # Verify methods were called the expected number of times
            assert mock_handle.call_count == 3
            assert mock_update.call_count == 3
            assert mock_render.call_count == 3
            
            # Verify clock.tick was called each iteration
            assert game.clock.tick.call_count == 3
            
            # Verify pygame.quit was called at the end
            mock_quit.assert_called_once()