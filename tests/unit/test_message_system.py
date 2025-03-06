# tests/unit/test_message_system.py
import pytest
import pygame
import time
from unittest.mock import MagicMock, patch

from rummikub.message_system import Message, MessageSystem

class TestMessage:
    """Unit tests for the Message class"""
    
    @pytest.fixture
    def mock_theme_manager(self):
        """Create a mock ThemeManager with necessary methods"""
        with patch('rummikub.message_system.ThemeManager') as mock_tm:
            # Mock the necessary methods
            mock_tm.get_font.return_value = MagicMock(spec=pygame.font.Font)
            mock_tm.get_font.return_value.render.return_value = MagicMock(spec=pygame.Surface)
            
            mock_tm.get_color.return_value = (255, 255, 255)  # White
            
            yield mock_tm
    
    def test_message_initialization(self):
        """Test message initialization with various parameters"""
        # Default parameters
        message = Message("Test message")
        assert message.text == "Test message"
        assert message.duration == 3.0
        assert message.color_name == "text"
        assert message.font_name == "normal"
        assert message.position is None
        assert message.alpha == 0  # Start transparent
        
        # Custom parameters
        message = Message(
            "Custom message", 
            duration=5.0, 
            color_name="warning", 
            font_name="bold", 
            position=(100, 200)
        )
        assert message.text == "Custom message"
        assert message.duration == 5.0
        assert message.color_name == "warning"
        assert message.font_name == "bold"
        assert message.position == (100, 200)
    
    def test_message_update_fade_in(self):
        """Test message update during fade-in period"""
        message = Message("Fade-in test", duration=3.0)
        
        # Set creation time to a known value
        message.creation_time = time.time() - 0.15  # 0.15 seconds into fade-in
        
        # Update the message
        is_active = message.update()
        
        # Should be active and halfway through fade-in
        assert is_active is True
        assert message.alpha == pytest.approx(127, abs=10)  # ~127 (50% of 255)
    
    def test_message_update_visible(self):
        """Test message update during fully visible period"""
        message = Message("Visible test", duration=3.0)
        
        # Set creation time to a known value
        message.creation_time = time.time() - 1.0  # 1 second in, fully visible
        
        # Update the message
        is_active = message.update()
        
        # Should be active and fully visible
        assert is_active is True
        assert message.alpha == 255
    
    def test_message_update_fade_out(self):
        """Test message update during fade-out period"""
        message = Message("Fade-out test", duration=3.0)
        
        # Set creation time to a known value
        message.creation_time = time.time() - 2.75  # 0.25 seconds from end
        
        # Update the message
        is_active = message.update()
        
        # Should be active and halfway through fade-out
        assert is_active is True
        assert message.alpha < 255
    
    def test_message_update_expired(self):
        """Test message update when message has expired"""
        message = Message("Expired test", duration=3.0)
        
        # Set creation time to a known value
        message.creation_time = time.time() - 3.5  # 0.5 seconds after expiration
        
        # Update the message
        is_active = message.update()
        
        # Should be inactive
        assert is_active is False
    
    def test_message_draw_default_position(self, mock_theme_manager):
        """Test drawing a message with default position"""
        message = Message("Draw test")
        message.alpha = 200  # Set alpha for testing
        
        # Create a mock surface
        mock_surface = MagicMock(spec=pygame.Surface)
        mock_surface.get_width.return_value = 800
        
        # Get mocked text surface
        text_surf = mock_theme_manager.get_font.return_value.render.return_value
        text_surf.get_width.return_value = 200
        
        # Draw the message
        message.draw(mock_surface)
        
        # Verify font and color were requested
        mock_theme_manager.get_font.assert_called_once_with("normal")
        mock_theme_manager.get_color.assert_called_once_with("text")
        
        # Verify text surface was created and had alpha set
        text_surf.set_alpha.assert_called_once_with(200)
        
        # Verify surface was blitted at calculated position (centered)
        expected_x = 300  # (800 - 200) / 2
        mock_surface.blit.assert_called_once()
        args, _ = mock_surface.blit.call_args
        assert args[1][0] == expected_x
        assert args[1][1] == 100  # Default y
    
    def test_message_draw_custom_position(self, mock_theme_manager):
        """Test drawing a message with custom position"""
        message = Message("Position test", position=(50, 60))
        message.alpha = 200  # Set alpha for testing
        
        # Create a mock surface
        mock_surface = MagicMock(spec=pygame.Surface)
        
        # Get mocked text surface
        text_surf = mock_theme_manager.get_font.return_value.render.return_value
        
        # Draw the message
        message.draw(mock_surface)
        
        # Verify surface was blitted at custom position
        mock_surface.blit.assert_called_once()
        args, _ = mock_surface.blit.call_args
        assert args[1] == (50, 60)


class TestMessageSystem:
    """Unit tests for the MessageSystem class"""
    
    @pytest.fixture
    def mock_message(self):
        """Create a mock Message class"""
        with patch('rummikub.message_system.Message') as MockMessage:
            message_instance = MagicMock()
            MockMessage.return_value = message_instance
            
            # Configure the update method to return True (active)
            message_instance.update.return_value = True
            
            yield MockMessage, message_instance
    
    def test_message_system_initialization(self):
        """Test MessageSystem initialization"""
        system = MessageSystem()
        assert system.messages == []
        assert system.max_messages == 3
        assert system.vertical_spacing == 50
    
    def test_add_message(self, mock_message):
        """Test adding messages to the system"""
        MockMessage, message_instance = mock_message
        
        system = MessageSystem()
        system.add_message("Test message")
        
        # Verify Message was created with correct parameters
        MockMessage.assert_called_once_with(
            "Test message", 3.0, "text", "normal", None
        )
        
        # Verify message was added to the list
        assert len(system.messages) == 1
        assert system.messages[0] is message_instance
    
    def test_add_message_with_custom_params(self, mock_message):
        """Test adding messages with custom parameters"""
        MockMessage, _ = mock_message
        
        system = MessageSystem()
        system.add_message(
            "Custom message", 
            duration=5.0, 
            color_name="warning", 
            font_name="bold", 
            position=(100, 200)
        )