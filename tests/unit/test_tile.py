# tests/unit/test_tile.py
import pytest
import pygame
import os
from unittest.mock import MagicMock, patch

from rummikub.tile import Tile

class TestTile:
    """Unit tests for the Tile class"""
    
    @pytest.fixture
    def mock_image(self):
        """Create a mock pygame image for testing"""
        mock_image = MagicMock(spec=pygame.Surface)
        mock_image.get_rect.return_value = pygame.Rect(0, 0, 130, 200)
        return mock_image
    
    @pytest.fixture
    def mock_transform(self):
        """Mock pygame transform module"""
        with patch('pygame.transform.smoothscale') as mock_scale:
            # Make smoothscale return a mock surface with the right size
            def side_effect(image, size):
                mock_surface = MagicMock(spec=pygame.Surface)
                mock_surface.get_rect.return_value = pygame.Rect(0, 0, size[0], size[1])
                return mock_surface
            
            mock_scale.side_effect = side_effect
            yield mock_scale
    
    @pytest.fixture
    def mock_theme_manager(self):
        """Mock ThemeManager"""
        with patch('rummikub.tile.ThemeManager') as mock_tm:
            mock_tm.get_color.return_value = (255, 0, 0, 128)  # Example color with alpha
            yield mock_tm
    
    @pytest.fixture
    def test_tile(self, mock_image, mock_transform):
        """Create a test tile with mocked dependencies"""
        with patch('pygame.image.load', return_value=mock_image):
            return Tile(1, 8, "red", "mock/path.png")
    
    @pytest.fixture
    def joker_tile(self, mock_image, mock_transform):
        """Create a joker tile with mocked dependencies"""
        with patch('pygame.image.load', return_value=mock_image):
            return Tile(2, 0, "black", "mock/joker.png", is_joker=True)
    
    def test_initialization_default(self, mock_image, mock_transform):
        """Test tile initialization with default parameters"""
        with patch('pygame.image.load', return_value=mock_image):
            tile = Tile(1, 8, "red", "mock/path.png")
            
            # Verify basic properties
            assert tile.id == 1
            assert tile.number == 8
            assert tile.color == "red"
            assert tile.is_joker is False
            assert tile.in_set is False
            
            # Verify default dimensions
            assert tile.width == Tile.DEFAULT_WIDTH
            assert tile.height == Tile.DEFAULT_HEIGHT
            
            # Verify initial state
            assert tile.dragging is False
            assert tile.highlight is False
            assert tile.highlight_color is None
            
            # Verify pygame.image.load was called
            pygame.image.load.assert_called_once_with("mock/path.png")
            
            # Verify transform.smoothscale was called with default dimensions
            mock_transform.assert_called_once_with(mock_image, (Tile.DEFAULT_WIDTH, Tile.DEFAULT_HEIGHT))
    
    def test_initialization_custom_size(self, mock_image, mock_transform):
        """Test tile initialization with custom dimensions"""
        with patch('pygame.image.load', return_value=mock_image):
            custom_width, custom_height = 150, 220
            tile = Tile(1, 8, "red", "mock/path.png", width=custom_width, height=custom_height)
            
            # Verify dimensions were set correctly
            assert tile.width == custom_width
            assert tile.height == custom_height
            
            # Verify transform.smoothscale was called with custom dimensions
            mock_transform.assert_called_once_with(mock_image, (custom_width, custom_height))
    
    def test_initialization_joker(self, mock_image, mock_transform):
        """Test joker tile initialization"""
        with patch('pygame.image.load', return_value=mock_image):
            tile = Tile(2, 0, "black", "mock/joker.png", is_joker=True)
            
            # Verify joker flag was set
            assert tile.is_joker is True
    
    @patch('pygame.transform.smoothscale')
    def test_resize_image(self, mock_transform, test_tile):
        """Test resizing the tile image"""
        # Set a specific return value for mock_transform
        mock_result = MagicMock(name="resized_surface")
        mock_transform.return_value = mock_result
        
        # Call resize_image with new dimensions
        new_width, new_height = 160, 240
        resized = test_tile.resize_image(new_width, new_height)
        
        # Verify transform.smoothscale was called with new dimensions
        mock_transform.assert_called_once_with(test_tile.original_image, (new_width, new_height))
        
        # Verify the returned image is the mock returned by smoothscale
        assert resized is mock_result
    
    def test_set_size(self, test_tile, mock_transform):
        """Test changing the tile size"""
        # Reset mock to clear previous calls
        mock_transform.reset_mock()
        
        # Save original center position
        original_center = test_tile.rect.center
        
        # Set new size
        new_width, new_height = 160, 240
        test_tile.set_size(new_width, new_height)
        
        # Verify dimensions were updated
        assert test_tile.width == new_width
        assert test_tile.height == new_height
        
        # Verify transform.smoothscale was called
        mock_transform.assert_called_once_with(test_tile.original_image, (new_width, new_height))
        
        # Verify rect was updated but center position maintained
        assert test_tile.rect.center == original_center
    
    def test_set_highlight(self, test_tile):
        """Test setting highlight state"""
        # Set highlight with a color
        test_tile.set_highlight(True, "valid")
        
        # Verify highlight state
        assert test_tile.highlight is True
        assert test_tile.highlight_color == "valid"
        
        # Clear highlight
        test_tile.set_highlight(False)
        
        # Verify highlight was cleared
        assert test_tile.highlight is False
    
    def test_draw_normal(self, test_tile):
        """Test drawing a tile normally"""
        # Create a mock screen
        mock_screen = MagicMock(spec=pygame.Surface)
        
        # Draw the tile
        test_tile.draw(mock_screen)
        
        # Verify screen.blit was called once with the right image and rect
        mock_screen.blit.assert_called_once_with(test_tile.image, test_tile.rect)
    
    def test_draw_highlighted(self, test_tile):
        """Test drawing a highlighted tile"""
        # Create a mock screen
        mock_screen = MagicMock()
        
        # Set highlight
        test_tile.set_highlight(True, "valid")
        
        # Create a mock for the highlight surface without using spec
        with patch('pygame.Surface', return_value=MagicMock()) as mock_surface_class:
            # Call the draw method
            test_tile.draw(mock_screen)
            
            # Verify Surface was created and blitted
            mock_surface_class.assert_called_once()
            assert mock_screen.blit.called
    
    def test_draw_dragging(self, test_tile, mock_transform):
        """Test drawing a tile while dragging (with scale effect)"""
        # Create a mock screen
        mock_screen = MagicMock(spec=pygame.Surface)
        
        # Set dragging state
        test_tile.dragging = True
        
        # Reset transform mock to clear previous calls
        mock_transform.reset_mock()
        
        # Draw the tile
        test_tile.draw(mock_screen)
        
        # Verify transform.smoothscale was called with scaled dimensions (110% of original)
        expected_width = int(test_tile.width * 1.1)
        expected_height = int(test_tile.height * 1.1)
        mock_transform.assert_called_once_with(test_tile.original_image, (expected_width, expected_height))
        
        # Verify scaled image was blitted
        mock_screen.blit.assert_called_once()
    
    def test_getters(self, test_tile):
        """Test all getter methods"""
        # Set up tile position
        test_tile.rect.x = 100
        test_tile.rect.y = 200
        
        # Test getters
        assert test_tile.get_id() == 1
        assert test_tile.get_number() == 8
        assert test_tile.get_color() == "red"
        assert test_tile.get_image() == test_tile.image
        assert test_tile.get_x() == 100
        assert test_tile.get_y() == 200
        assert test_tile.get_coordinates() == (100, 200)
        assert test_tile.get_size() == (Tile.DEFAULT_WIDTH, Tile.DEFAULT_HEIGHT)
    
    def test_setters(self, test_tile):
        """Test coordinate setter methods"""
        # Test set_x
        test_tile.set_x(150)
        assert test_tile.rect.x == 150
        
        # Test set_y
        test_tile.set_y(250)
        assert test_tile.rect.y == 250
        
        # Test set_coordinates
        test_tile.set_coordinates(300, 400)
        assert test_tile.rect.x == 300
        assert test_tile.rect.y == 400
    
    def test_position_saving(self, test_tile):
        """Test position saving methods"""
        # Set initial position
        test_tile.set_coordinates(100, 200)
        
        # Save pre-drag position
        test_tile.save_pre_drag_pos()
        assert test_tile.pre_drag_pos == (100, 200)
        
        # Move tile
        test_tile.set_coordinates(300, 400)
        
        # Get pre-drag position
        assert test_tile.get_pre_drag_pos() == (100, 200)
        
        # Save turn start position
        test_tile.save_turn_start_position()
        assert test_tile.turn_start_pos == (300, 400)
    
    def test_dragging(self, test_tile):
        """Test dragging functionality"""
        # Set initial position
        test_tile.set_coordinates(100, 200)
        
        # Start dragging from mouse position (105, 205) - should set a (5, 5) offset
        test_tile.start_drag((105, 205))
        
        # Verify dragging state
        assert test_tile.dragging is True
        assert test_tile.pre_drag_pos == (100, 200)
        assert test_tile.drag_offset == (-5, -5)
        
        # Update drag to a new mouse position
        test_tile.update_drag((200, 300))
        
        # Verify position was updated
        assert test_tile.rect.x == 195  # 200 - 5
        assert test_tile.rect.y == 295  # 300 - 5
        
        # Stop dragging
        test_tile.stop_drag()
        assert test_tile.dragging is False
    
    def test_revert_positions(self, test_tile):
        """Test position reversion functionality"""
        # Set initial position and save it
        test_tile.set_coordinates(100, 200)
        test_tile.save_turn_start_position()
        
        # Move tile and save pre-drag
        test_tile.set_coordinates(300, 400)
        test_tile.save_pre_drag_pos()
        
        # Move tile again
        test_tile.set_coordinates(500, 600)
        
        # Revert to pre-drag
        test_tile.revert_to_pre_drag()
        assert test_tile.rect.x == 300
        assert test_tile.rect.y == 400
        
        # Revert to turn start
        test_tile.revert_to_turn_start()
        assert test_tile.rect.x == 100
        assert test_tile.rect.y == 200
    
    def test_reset_joker_for_joker_tile(self, joker_tile):
        """Test resetting a joker tile"""
        # Set joker as part of a set with a value
        joker_tile.number = 7
        joker_tile.in_set = True
        
        # Reset the joker
        joker_tile.reset_joker()
        
        # Verify joker was reset
        assert joker_tile.number == 0
        assert joker_tile.in_set is False
    
    def test_reset_joker_for_normal_tile(self, test_tile):
        """Test that reset_joker does nothing for normal tiles"""
        # Set initial state
        test_tile.number = 8
        
        # Try to reset a non-joker
        test_tile.reset_joker()
        
        # Verify tile was not affected
        assert test_tile.number == 8