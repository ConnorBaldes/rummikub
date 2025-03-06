# tests/unit/test_game_screen.py
import pytest
import pygame
from unittest.mock import MagicMock, patch, call

from rummikub.screens.game_screen import GameScreen
from rummikub.tile import Tile
from rummikub.board import Board
from rummikub.player import Player
from rummikub.theme_manager import ThemeManager
from rummikub.message_system import MessageSystem

class TestGameScreen:
    """Unit tests for the GameScreen class"""
    
    @pytest.fixture
    def mock_pygame(self):
        """Mock pygame to avoid actual initialization"""
        with patch('pygame.display.set_mode') as mock_set_mode, \
             patch('pygame.image.load') as mock_load, \
             patch('pygame.Surface') as mock_surface, \
             patch('pygame.mixer.init') as mock_mixer_init, \
             patch('pygame.mixer.Sound') as mock_sound:
                
            # Configure mocks
            mock_screen = MagicMock()
            mock_screen.get_width.return_value = 3400
            mock_screen.get_height.return_value = 2500
            mock_set_mode.return_value = mock_screen
            
            # Mock image load to return consistent surfaces
            def mock_load_image(path):
                mock_img = MagicMock()
                mock_img.get_rect.return_value = pygame.Rect(0, 0, 200, 100)
                return mock_img
            mock_load.side_effect = mock_load_image
            
            # Mock Surface to return a usable surface
            mock_surface_instance = MagicMock()
            mock_surface.return_value = mock_surface_instance
            
            # Mock Sound to return a playable sound
            mock_sound_instance = MagicMock()
            mock_sound.return_value = mock_sound_instance
            
            yield {
                'set_mode': mock_set_mode,
                'screen': mock_screen,
                'load': mock_load,
                'surface': mock_surface_instance,
                'mixer_init': mock_mixer_init,
                'sound': mock_sound_instance
            }
    
    @pytest.fixture
    def mock_theme_manager(self):
        """Mock ThemeManager to avoid actual rendering"""
        with patch('rummikub.screens.game_screen.ThemeManager') as MockTM:
            # Configure color getter
            MockTM.get_color.return_value = (100, 100, 100, 255)
            
            # Configure text renderer
            mock_text_surface = MagicMock()
            MockTM.render_text.return_value = mock_text_surface
            
            # Configure button drawer
            MockTM.draw_button = MagicMock()
            
            yield MockTM
    
    @pytest.fixture
    def mock_message_system(self):
        """Mock MessageSystem to avoid actual message handling"""
        with patch('rummikub.screens.game_screen.MessageSystem') as MockMS:
            mock_ms_instance = MagicMock(spec=MessageSystem)
            MockMS.return_value = mock_ms_instance
            yield mock_ms_instance
    
    @pytest.fixture
    def mock_board(self):
        """Mock Board to avoid actual board management"""
        with patch('rummikub.screens.game_screen.Board') as MockBoard:
            mock_board_instance = MagicMock(spec=Board)
            mock_board_instance.tiles = {}
            mock_board_instance.added_tiles = []
            MockBoard.return_value = mock_board_instance
            yield mock_board_instance
    
    @pytest.fixture
    def mock_game(self):
        """Create a mock game object with necessary properties"""
        game = MagicMock()
        
        # Configure players
        player1 = MagicMock(spec=Player)
        player1.name = "Player 1"
        player1.tiles = {}
        player1.draw_tile = MagicMock()
        
        player2 = MagicMock(spec=Player)
        player2.name = "Player 2"
        player2.tiles = {}
        
        game.players = [player1, player2]
        game.current_turn = 0
        
        # Configure statistics
        game.statistics = {
            'turns_played': 0,
            'tiles_drawn': 0,
            'valid_sets_formed': 0,
            'invalid_moves': 0
        }
        
        # Configure deck
        mock_deck = MagicMock()
        mock_deck.__len__ = MagicMock(return_value=53)
        game.deck = mock_deck
        
        # Configure validation methods
        game.validate_turn = MagicMock(return_value=True)
        game.check_for_win = MagicMock(return_value=False)
        
        return game
    
    @pytest.fixture
    def game_screen(self, mock_pygame, mock_theme_manager, mock_message_system, mock_board, mock_game):
        """Create a GameScreen instance with mocked dependencies"""
        # Create instance
        screen = GameScreen(mock_game)
        
        # Replace board with our mock
        screen.board = mock_board
        
        # Reset mocks to clear initialization calls
        mock_message_system.reset_mock()
        mock_board.reset_mock()
        
        return screen
    
    @pytest.fixture
    def mock_tiles(self):
        """Create mock tiles for testing"""
        def _create_tile(tile_id, number, color, x=0, y=0, is_joker=False):
            # Create the base mock tile
            tile = MagicMock()
            tile.id = tile_id
            tile.number = number
            tile.color = color
            tile.is_joker = is_joker
            tile.in_set = False
            tile.dragging = False
            tile.highlight = False
            tile.highlight_color = None
            tile.scale_factor = 1.0
            tile.width = Tile.DEFAULT_WIDTH
            tile.height = Tile.DEFAULT_HEIGHT
            
            # Create a mock rect with properly mocked collidepoint
            mock_rect = MagicMock()
            mock_rect.x = x
            mock_rect.y = y
            mock_rect.width = tile.width
            mock_rect.height = tile.height
            mock_rect.center = (x + tile.width//2, y + tile.height//2)
            # Make collidepoint return True if the point is within the rect bounds
            mock_rect.collidepoint.side_effect = lambda pos: (
                x <= pos[0] <= x + tile.width and
                y <= pos[1] <= y + tile.height
            )
            
            tile.rect = mock_rect
            
            # Set up positions
            tile.turn_start_pos = (x, y)
            tile.pre_drag_pos = (x, y)
            tile.drag_offset = (0, 0)
            
            # Set up mock methods
            tile.get_id.return_value = tile_id
            tile.get_number.return_value = number
            tile.get_color.return_value = color
            tile.get_x.return_value = x
            tile.get_y.return_value = y
            tile.get_coordinates.return_value = (x, y)
            tile.get_size.return_value = (tile.width, tile.height)
            tile.get_pre_drag_pos.return_value = (x, y)
            
            # Set setters to update the rect
            def set_x(new_x):
                tile.rect.x = new_x
                return None
            
            def set_y(new_y):
                tile.rect.y = new_y
                return None
            
            def set_coordinates(new_x, new_y):
                tile.rect.x = new_x
                tile.rect.y = new_y
                return None
            
            def start_drag(mouse_pos):
                tile.dragging = True
                tile.pre_drag_pos = (tile.rect.x, tile.rect.y)
                tile.drag_offset = (tile.rect.x - mouse_pos[0], tile.rect.y - mouse_pos[1])
            
            def stop_drag():
                tile.dragging = False
            
            def revert_to_pre_drag():
                tile.rect.x = tile.pre_drag_pos[0]
                tile.rect.y = tile.pre_drag_pos[1]
            
            def revert_to_turn_start():
                tile.rect.x = tile.turn_start_pos[0]
                tile.rect.y = tile.turn_start_pos[1]
            
            def save_turn_start_position():
                tile.turn_start_pos = (tile.rect.x, tile.rect.y)
            
            def save_pre_drag_pos():
                tile.pre_drag_pos = (tile.rect.x, tile.rect.y)
            
            def reset_joker():
                if tile.is_joker:
                    tile.number = 0
                    tile.in_set = False
            
            # Assign the method mocks
            tile.set_x.side_effect = set_x
            tile.set_y.side_effect = set_y
            tile.set_coordinates.side_effect = set_coordinates
            tile.start_drag.side_effect = start_drag
            tile.stop_drag.side_effect = stop_drag
            tile.revert_to_pre_drag.side_effect = revert_to_pre_drag
            tile.revert_to_turn_start.side_effect = revert_to_turn_start
            tile.save_turn_start_position.side_effect = save_turn_start_position
            tile.save_pre_drag_pos.side_effect = save_pre_drag_pos
            tile.reset_joker.side_effect = reset_joker
            
            # Draw method doesn't need any particular implementation for testing
            tile.draw.return_value = None
            
            return tile
        
        return _create_tile
    
    def test_initialization(self, mock_pygame, mock_theme_manager, mock_message_system, mock_board, mock_game):
        """Test GameScreen initialization"""
        # Create GameScreen
        screen = GameScreen(mock_game)
        
        # Verify pygame display setup
        mock_pygame['set_mode'].assert_called_once_with((3400, 2500))
        
        # Verify theme manager initialization
        mock_theme_manager.initialize.assert_called_once()
        
        # Verify message system creation
        assert isinstance(screen.message_system, MagicMock)
        
        # Verify board creation
        assert isinstance(screen.board, MagicMock)
        
        # Verify image loading
        expected_image_paths = [
            "./rummikub/assets/buttons/draw_button.png",
            "./rummikub/assets/buttons/end_turn_button.png",
            "./rummikub/assets/buttons/reset_button.png",
            "./rummikub/assets/rack.png"
        ]
        
        # Check that image load was called for each expected path
        # Account for possible exception when loading reset button
        for path in expected_image_paths[:2] + expected_image_paths[3:]:
            assert any(call(path) == c for c in mock_pygame['load'].call_args_list)
        
        # Verify button hover states initialization
        assert screen.draw_button_hover == False
        assert screen.end_button_hover == False
        assert screen.reset_button_hover == False
        
        # Verify sound initialization
        assert screen.sound_enabled == True
    
    def test_initialization_with_missing_reset_button(self, mock_pygame, mock_theme_manager, mock_message_system, mock_board, mock_game):
        """Test initialization with missing reset button image"""
        # Configure image load to raise exception for reset button
        def mock_load_image(path):
            if "reset_button.png" in path:
                raise FileNotFoundError("File not found")
            mock_img = MagicMock()
            mock_img.get_rect.return_value = pygame.Rect(0, 0, 200, 100)
            return mock_img
        
        mock_pygame['load'].side_effect = mock_load_image
        
        # Create GameScreen
        screen = GameScreen(mock_game)
        
        # Verify pygame Surface was called to create replacement
        assert mock_pygame['surface'].fill.called
    
    def test_initialization_with_sound_disabled(self, mock_pygame, mock_theme_manager, mock_message_system, mock_board, mock_game):
        """Test initialization with sound system failure"""
        # Configure mixer.init to raise exception
        mock_pygame['mixer_init'].side_effect = pygame.error("Mixer initialization failed")
        
        # Patch print to capture output
        with patch('builtins.print') as mock_print:
            # Create GameScreen
            screen = GameScreen(mock_game)
            
            # Verify sound is disabled
            assert screen.sound_enabled == False
            
            # Verify error message was printed
            mock_print.assert_called_once_with("Sound system initialization failed. Sounds disabled.")
    
    def test_load_sounds(self, game_screen, mock_pygame):
        """Test loading game sound effects"""
        # Reset mock to clear initialization calls
        mock_pygame['sound'].reset_mock()
        
        # Call load_sounds (although it should be called in __init__)
        game_screen.load_sounds()
        
        # Verify Sound constructor was called for each expected sound
        expected_sound_paths = [
            './rummikub/assets/sounds/tile_place.wav',
            './rummikub/assets/sounds/invalid_move.wav',
            './rummikub/assets/sounds/draw_tile.wav',
            './rummikub/assets/sounds/valid_set.wav',
            './rummikub/assets/sounds/win.wav'
        ]
        
        # Check that Sound was created for each path
        for path in expected_sound_paths:
            assert any(call(path) == c for c in mock_pygame['sound'].call_args_list)
        
        # Verify all sounds were loaded
        assert len(game_screen.sounds) == 5
        assert all(name in game_screen.sounds for name in [
            'tile_place', 'invalid_move', 'draw_tile', 'valid_set', 'win'
        ])
    
    def test_play_sound_enabled(self, game_screen):
        """Test playing a sound when enabled"""
        # Ensure sound is enabled
        game_screen.sound_enabled = True
        
        # Create mock sound
        mock_sound = MagicMock()
        game_screen.sounds = {'test_sound': mock_sound}
        
        # Play sound
        game_screen.play_sound('test_sound')
        
        # Verify sound.play was called
        mock_sound.play.assert_called_once()
    
    def test_play_sound_disabled(self, game_screen):
        """Test playing a sound when disabled"""
        # Disable sound
        game_screen.sound_enabled = False
        
        # Create mock sound
        mock_sound = MagicMock()
        game_screen.sounds = {'test_sound': mock_sound}
        
        # Play sound
        game_screen.play_sound('test_sound')
        
        # Verify sound.play was not called
        mock_sound.play.assert_not_called()
    
    def test_play_sound_nonexistent(self, game_screen):
        """Test playing a non-existent sound"""
        # Ensure sound is enabled
        game_screen.sound_enabled = True
        
        # Create mock sound
        mock_sound = MagicMock()
        game_screen.sounds = {'test_sound': mock_sound}
        
        # Play non-existent sound
        game_screen.play_sound('nonexistent_sound')
        
        # Verify sound.play was not called
        mock_sound.play.assert_not_called()
    
    def test_handle_events_button_hover(self, game_screen):
        """Test button hover states in handle_events"""
        # Create mouse events with different positions
        events = []
        
        # Mock button rects for testing hover
        game_screen.draw_button_rect = pygame.Rect(50, 50, 100, 50)
        game_screen.end_button_rect = pygame.Rect(50, 150, 100, 50)
        game_screen.reset_button_rect = pygame.Rect(50, 250, 100, 50)
        
        # Mock mouse position
        with patch('pygame.mouse.get_pos', return_value=(75, 75)):
            # Handle events
            game_screen.handle_events(events)
            
            # Verify hover states
            assert game_screen.draw_button_hover == True
            assert game_screen.end_button_hover == False
            assert game_screen.reset_button_hover == False
        
        # Move mouse to end button
        with patch('pygame.mouse.get_pos', return_value=(75, 175)):
            # Handle events
            game_screen.handle_events(events)
            
            # Verify hover states
            assert game_screen.draw_button_hover == False
            assert game_screen.end_button_hover == True
            assert game_screen.reset_button_hover == False
    
    def test_handle_events_draw_button_click(self, game_screen):
        """Test clicking the draw button"""
        # Mock button rect
        game_screen.draw_button_rect = pygame.Rect(50, 50, 100, 50)
        
        # Create mouse click event
        event = MagicMock()
        event.type = pygame.MOUSEBUTTONDOWN
        
        # Mock mouse position to be on the draw button
        with patch('pygame.mouse.get_pos', return_value=(75, 75)), \
             patch.object(game_screen, 'play_sound') as mock_play_sound:
            
            # Set up board state - no tiles added
            game_screen.board.added_tiles = []
            
            # Handle event
            game_screen.handle_events([event])
            
            # Verify player draws tile
            game_screen.game.players[0].draw_tile.assert_called_once()
            
            # Verify message was added
            game_screen.message_system.add_message.assert_called_with(
                f"{game_screen.game.players[0].name} drew a tile.",
                color_name='highlight'
            )
            
            # Verify statistics updated
            assert game_screen.game.statistics['tiles_drawn'] == 1
            
            # Verify sound played
            mock_play_sound.assert_called_with('draw_tile')
            
            # Verify next turn called
            game_screen.game.next_turn.assert_called_once()
    
    def test_handle_events_draw_button_click_with_tiles_on_board(self, game_screen):
        """Test clicking the draw button when tiles are on the board"""
        # Mock button rect
        game_screen.draw_button_rect = pygame.Rect(50, 50, 100, 50)
        
        # Create mouse click event
        event = MagicMock()
        event.type = pygame.MOUSEBUTTONDOWN
        
        # Mock mouse position to be on the draw button
        with patch('pygame.mouse.get_pos', return_value=(75, 75)), \
             patch.object(game_screen, 'play_sound') as mock_play_sound:
            
            # Set up board state - tiles added
            game_screen.board.added_tiles = [1, 2, 3]
            
            # Handle event
            game_screen.handle_events([event])
            
            # Verify player does not draw tile
            game_screen.game.players[0].draw_tile.assert_not_called()
            
            # Verify error message was added
            game_screen.message_system.add_message.assert_called_with(
                "Cannot draw while tiles are on the board!",
                color_name='invalid'
            )
            
            # Verify sound played
            mock_play_sound.assert_called_with('invalid_move')
            
            # Verify next turn not called
            game_screen.game.next_turn.assert_not_called()
    
    def test_handle_events_end_button_click_valid(self, game_screen):
        """Test clicking the end button with a valid move"""
        # Mock button rect
        game_screen.end_button_rect = pygame.Rect(50, 150, 100, 50)
        
        # Create mouse click event
        event = MagicMock()
        event.type = pygame.MOUSEBUTTONDOWN
        
        # Configure game to return valid turn and no win
        game_screen.game.validate_turn.return_value = True
        game_screen.game.check_for_win.return_value = False
        
        # Mock mouse position to be on the end button
        with patch('pygame.mouse.get_pos', return_value=(75, 175)), \
             patch.object(game_screen, 'play_sound') as mock_play_sound:
            
            # Handle event
            game_screen.handle_events([event])
            
            # Verify validate_turn was called
            game_screen.game.validate_turn.assert_called_once()
            
            # Verify check_for_win was called
            game_screen.game.check_for_win.assert_called_once()
            
            # Verify message was added
            game_screen.message_system.add_message.assert_called_with(
                "Valid move! Turn completed.",
                color_name='valid'
            )
            
            # Verify sound played
            mock_play_sound.assert_called_with('valid_set')
            
            # Verify next turn called
            game_screen.game.next_turn.assert_called_once()
    
    def test_handle_events_end_button_click_invalid(self, game_screen):
        """Test clicking the end button with an invalid move"""
        # Mock button rect
        game_screen.end_button_rect = pygame.Rect(50, 150, 100, 50)
        
        # Create mouse click event
        event = MagicMock()
        event.type = pygame.MOUSEBUTTONDOWN
        
        # Configure game to return invalid turn
        game_screen.game.validate_turn.return_value = False
        
        # Mock mouse position to be on the end button
        with patch('pygame.mouse.get_pos', return_value=(75, 175)), \
             patch.object(game_screen, 'play_sound') as mock_play_sound:
            
            # Handle event
            game_screen.handle_events([event])
            
            # Verify validate_turn was called
            game_screen.game.validate_turn.assert_called_once()
            
            # Verify check_for_win was not called
            game_screen.game.check_for_win.assert_not_called()
            
            # Verify message was added
            game_screen.message_system.add_message.assert_called_with(
                "Invalid move! Use Reset button to return tiles to previous positions.",
                color_name='invalid'
            )
            
            # Verify invalid moves statistic incremented
            assert game_screen.game.statistics['invalid_moves'] == 1
            
            # Verify sound played
            mock_play_sound.assert_called_with('invalid_move')
            
            # Verify next turn not called
            game_screen.game.next_turn.assert_not_called()
    
    def test_handle_events_end_button_click_win(self, game_screen):
        """Test clicking the end button resulting in a win"""
        # Mock button rect
        game_screen.end_button_rect = pygame.Rect(50, 150, 100, 50)
        
        # Create mouse click event
        event = MagicMock()
        event.type = pygame.MOUSEBUTTONDOWN
        
        # Configure game to return valid turn and win
        game_screen.game.validate_turn.return_value = True
        game_screen.game.check_for_win.return_value = True
        
        # Mock mouse position to be on the end button
        with patch('pygame.mouse.get_pos', return_value=(75, 175)), \
             patch.object(game_screen, 'play_sound') as mock_play_sound:
            
            # Handle event
            game_screen.handle_events([event])
            
            # Verify validate_turn was called
            game_screen.game.validate_turn.assert_called_once()
            
            # Verify check_for_win was called
            game_screen.game.check_for_win.assert_called_once()
            
            # Verify win message was added
            assert any("wins the game" in call.args[0] for call in 
                       game_screen.message_system.add_message.call_args_list)
            
            # Verify sound played
            mock_play_sound.assert_called_with('win')
            
            # Verify next turn not called (game is over)
            game_screen.game.next_turn.assert_not_called()
    
    def test_handle_events_reset_button_click(self, game_screen):
        """Test clicking the reset button"""
        # Mock button rect
        game_screen.reset_button_rect = pygame.Rect(50, 250, 100, 50)
        
        # Create mouse click event
        event = MagicMock()
        event.type = pygame.MOUSEBUTTONDOWN
        
        # Mock mouse position to be on the reset button
        with patch('pygame.mouse.get_pos', return_value=(75, 275)), \
             patch.object(game_screen, 'play_sound') as mock_play_sound:
            
            # Handle event
            game_screen.handle_events([event])
            
            # Verify board.reset_board was called
            game_screen.board.reset_board.assert_called_once()
            
            # Verify message was added
            game_screen.message_system.add_message.assert_called_with(
                "Tiles reset to start of turn.",
                color_name='highlight'
            )
            
            # Verify sound played
            mock_play_sound.assert_called_with('tile_place')
    
    def test_handle_events_drag_start_from_rack(self, game_screen, mock_tiles):
        """Test starting to drag a tile from the player's rack"""
        # Create a tile in the player's rack
        tile = mock_tiles(1, 8, "red", x=100, y=2100)
        game_screen.game.players[0].tiles = {1: tile}

        # Create mouse click event
        event = MagicMock()
        event.type = pygame.MOUSEBUTTONDOWN

        # Mock mouse position to be on the tile (within tile's rect)
        with patch('pygame.mouse.get_pos', return_value=(120, 2150)):
            # Handle the event (collidepoint will now return True for this position)
            game_screen.handle_events([event])
            
            # Assert that the tile was selected for dragging
            assert game_screen.dragged_tile == tile
            assert game_screen.dragged_from == "rack"
            
            # Verify that start_drag was called with the correct position
            tile.start_drag.assert_called_once_with((120, 2150))
    
    def test_handle_events_drag_start_from_board(self, game_screen, mock_tiles):
        """Test starting to drag a tile from the board"""
        # Create a tile on the board
        tile = mock_tiles(1, 8, "red", x=200, y=300)
        game_screen.board.tiles = {1: tile}
        
        # Create mouse click event
        event = MagicMock()
        event.type = pygame.MOUSEBUTTONDOWN
        
        # Mock mouse position to be on the tile
        with patch('pygame.mouse.get_pos', return_value=(220, 350)):
            # Configure tile.rect.collidepoint to return True
            tile.rect.collidepoint.return_value = True
            
            # Configure player tiles to return empty to ensure board is checked
            game_screen.game.players[0].tiles = {}
            
            # Handle event
            game_screen.handle_events([event])
            
            # Verify tile.start_drag was called
            tile.start_drag.assert_called_once_with((220, 350))
            
            # Verify dragged_tile and dragged_from were set
            assert game_screen.dragged_tile == tile
            assert game_screen.dragged_from == 'board'
    
    def test_handle_events_drag_motion(self, game_screen, mock_tiles):
        """Test dragging a tile"""
        # Create a tile and set as dragged_tile
        tile = mock_tiles(1, 8, "red", x=200, y=300)
        game_screen.dragged_tile = tile
        game_screen.dragged_from = 'rack'
        
        # Create mouse motion event
        event = MagicMock()
        event.type = pygame.MOUSEMOTION
        
        # Mock mouse position
        mouse_pos = (250, 350)
        
        # Mock is_on_board to return True and is_valid_drop to return True
        with patch('pygame.mouse.get_pos', return_value=mouse_pos), \
             patch.object(game_screen, 'is_on_board', return_value=True), \
             patch.object(game_screen, 'is_valid_drop', return_value=True):
            
            # Handle event
            game_screen.handle_events([event])
            
            # Verify tile.update_drag was called
            tile.update_drag.assert_called_once_with(mouse_pos)
            
            # Verify highlight was set to valid
            tile.set_highlight.assert_called_once_with(True, 'valid')
    
    def test_handle_events_drag_motion_invalid(self, game_screen, mock_tiles):
        """Test dragging a tile to an invalid position"""
        # Create a tile and set as dragged_tile
        tile = mock_tiles(1, 8, "red", x=200, y=300)
        game_screen.dragged_tile = tile
        game_screen.dragged_from = 'rack'
        
        # Create mouse motion event
        event = MagicMock()
        event.type = pygame.MOUSEMOTION
        
        # Mock mouse position
        mouse_pos = (250, 350)
        
        # Mock is_on_board to return True and is_valid_drop to return False
        with patch('pygame.mouse.get_pos', return_value=mouse_pos), \
             patch.object(game_screen, 'is_on_board', return_value=True), \
             patch.object(game_screen, 'is_valid_drop', return_value=False):
            
            # Handle event
            game_screen.handle_events([event])
            
            # Verify tile.update_drag was called
            tile.update_drag.assert_called_once_with(mouse_pos)
            
            # Verify highlight was set to invalid
            tile.set_highlight.assert_called_once_with(True, 'invalid')
    
    def test_handle_events_drag_end_rack_to_board_valid(self, game_screen, mock_tiles):
        """Test dropping a tile from rack to board (valid)"""
        # Create a tile and set as dragged_tile
        tile = mock_tiles(1, 8, "red", x=200, y=300)
        game_screen.dragged_tile = tile
        game_screen.dragged_from = 'rack'
        
        # Add tile to player
        game_screen.game.players[0].tiles = {1: tile}
        
        # Create mouse button up event
        event = MagicMock()
        event.type = pygame.MOUSEBUTTONUP
        
        # Mock is_on_board to return True and is_valid_drop to return True
        with patch.object(game_screen, 'is_on_board', return_value=True), \
             patch.object(game_screen, 'is_valid_drop', return_value=True), \
             patch.object(game_screen, 'play_sound') as mock_play_sound:
            
            # Handle event
            game_screen.handle_events([event])
            
            # Verify tile.stop_drag and set_highlight were called
            tile.stop_drag.assert_called_once()
            tile.set_highlight.assert_called_with(False)
            
            # Verify player.remove_tile was called
            game_screen.game.players[0].remove_tile.assert_called_once_with(1)
            
            # Verify board.add_tile was called
            game_screen.board.add_tile.assert_called_once_with(tile)
            
            # Verify board.update_sets was called
            game_screen.board.update_sets.assert_called_once()
            
            # Verify board.snap_tile was called
            game_screen.board.snap_tile.assert_called_once_with(tile)
            
            # Verify sound played
            mock_play_sound.assert_called_with('tile_place')
            
            # Verify dragged_tile and dragged_from were reset
            assert game_screen.dragged_tile is None
            assert game_screen.dragged_from is None
    
    def test_handle_events_drag_end_rack_to_board_invalid(self, game_screen, mock_tiles):
        """Test dropping a tile from rack to board (invalid)"""
        # Create a tile and set as dragged_tile
        tile = mock_tiles(1, 8, "red", x=200, y=300)
        game_screen.dragged_tile = tile
        game_screen.dragged_from = 'rack'
        
        # Create mouse button up event
        event = MagicMock()
        event.type = pygame.MOUSEBUTTONUP
        
        # Mock is_on_board to return True and is_valid_drop to return False
        with patch.object(game_screen, 'is_on_board', return_value=True), \
             patch.object(game_screen, 'is_valid_drop', return_value=False), \
             patch.object(game_screen, 'play_sound') as mock_play_sound:
            
            # Handle event
            game_screen.handle_events([event])
            
            # Verify tile.stop_drag and set_highlight were called
            tile.stop_drag.assert_called_once()
            tile.set_highlight.assert_called_with(False)
            
            # Verify tile.revert_to_pre_drag was called
            tile.revert_to_pre_drag.assert_called_once()
            
            # Verify board.add_tile was not called
            game_screen.board.add_tile.assert_not_called()
            
            # Verify sound played
            mock_play_sound.assert_called_with('invalid_move')
    
    def test_handle_events_drag_end_board_to_rack(self, game_screen, mock_tiles):
        """Test dropping a tile from board to rack"""
        # Create a tile and set as dragged_tile
        tile = mock_tiles(1, 8, "red", x=200, y=300)
        game_screen.dragged_tile = tile
        game_screen.dragged_from = 'board'
        
        # Configure board
        game_screen.board.tiles = {1: tile}
        game_screen.board.added_tiles = [1]
        game_screen.board.remove_tile.return_value = tile
        
        # Create mouse button up event
        event = MagicMock()
        event.type = pygame.MOUSEBUTTONUP
        
        # Mock is_on_board to return False
        with patch.object(game_screen, 'is_on_board', return_value=False), \
             patch.object(game_screen, 'play_sound') as mock_play_sound:
            
            # Handle event
            game_screen.handle_events([event])
            
            # Verify tile.stop_drag and set_highlight were called
            tile.stop_drag.assert_called_once()
            tile.set_highlight.assert_called_with(False)
            
            # Verify board.remove_tile was called
            game_screen.board.remove_tile.assert_called_once_with(1)
            
            # Verify player.add_tile was called
            game_screen.game.players[0].add_tile.assert_called_once_with(tile)
            
            # Verify sound played
            mock_play_sound.assert_called_with('tile_place')
    
    def test_update(self, game_screen):
        """Test the update method"""
        # Call update
        game_screen.update()
        
        # Verify message_system.update was called
        game_screen.message_system.update.assert_called_once()
    
    def test_render(self, game_screen, mock_theme_manager):
        """Test the render method"""
        # Prepare mocks for pygame display
        with patch('pygame.display.update') as mock_update:
            # Call render
            game_screen.render()
            
            # Verify screen.fill was called
            game_screen.screen.fill.assert_called_once()
            
            # Verify screen.blit was called multiple times
            assert game_screen.screen.blit.call_count > 0
            
            # Verify ThemeManager.render_text was called
            assert mock_theme_manager.render_text.call_count > 0
            
            # Verify ThemeManager.draw_button was called for each button
            assert mock_theme_manager.draw_button.call_count >= 3
            
            # Verify message_system.draw was called
            game_screen.message_system.draw.assert_called_once_with(game_screen.screen)
            
            # Verify pygame.display.update was called
            mock_update.assert_called_once()
    
    def test_draw_player_tiles(self, game_screen):
        """Test drawing player tiles"""
        # Call draw_player_tiles
        game_screen.draw_player_tiles()
        
        # Verify current player's draw method was called
        game_screen.game.players[game_screen.game.current_turn].draw.assert_called_once_with(game_screen.screen)
    
    def test_is_on_board(self, game_screen):
        """Test the is_on_board method"""
        # Create test tiles
        tile_on_board = MagicMock()
        tile_on_board.x = 1000
        tile_on_board.y = 1000
        
        tile_off_board_x = MagicMock()
        tile_off_board_x.x = 4000  # > 3400
        tile_off_board_x.y = 1000
        
        tile_off_board_y = MagicMock()
        tile_off_board_y.x = 1000
        tile_off_board_y.y = 2000  # > 1760
        
        # Test each tile
        assert game_screen.is_on_board(tile_on_board) == True
        assert game_screen.is_on_board(tile_off_board_x) == False
        assert game_screen.is_on_board(tile_off_board_y) == False
    
    def test_is_valid_drop(self, game_screen):
        """Test the is_valid_drop method"""
        # Create test tiles
        tile1 = MagicMock()
        tile1.id = 1
        tile1.rect = pygame.Rect(100, 100, 140, 200)
        
        tile2 = MagicMock()
        tile2.id = 2
        tile2.rect = pygame.Rect(300, 100, 140, 200)  # Not colliding
        
        tile3 = MagicMock()
        tile3.id = 3
        tile3.rect = pygame.Rect(150, 150, 140, 200)  # Colliding with tile1
        
        # Container with non-colliding tiles
        container1 = {1: tile1, 2: tile2}
        
        # Container with colliding tiles
        container2 = {1: tile1, 3: tile3}
        
        # Test dragging tile2 over container1 (valid - no collision)
        assert game_screen.is_valid_drop(tile2, container1) == True
        
        # Test dragging tile3 over container1 (invalid - collides with tile1)
        assert game_screen.is_valid_drop(tile3, container1) == False