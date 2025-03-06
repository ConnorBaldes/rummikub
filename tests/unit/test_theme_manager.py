# tests/unit/test_theme_manager.py
import pytest
import pygame
from unittest.mock import MagicMock, patch

from rummikub.theme_manager import ThemeManager

class TestThemeManager:
    """Unit tests for the ThemeManager class"""
    
    @pytest.fixture
    def reset_font_cache(self):
        """Reset the font cache before and after each test"""
        ThemeManager._font_cache = {}
        yield
        ThemeManager._font_cache = {}
    
    @pytest.fixture
    def mock_pygame_font(self):
        """Mock pygame.font to avoid actual font loading"""
        with patch('pygame.font.init') as mock_init:
            with patch('pygame.font.SysFont') as mock_sysfont:
                # Make SysFont return a mock font
                mock_font = MagicMock()
                mock_font.render.return_value = MagicMock(spec=pygame.Surface)
                mock_sysfont.return_value = mock_font
                
                yield mock_init, mock_sysfont, mock_font
    
    def test_initialize(self, reset_font_cache, mock_pygame_font):
        """Test initializing the ThemeManager font cache"""
        mock_init, mock_sysfont, _ = mock_pygame_font
        
        # Initialize ThemeManager
        ThemeManager.initialize()
        
        # Verify pygame.font.init was called
        mock_init.assert_called_once()
        
        # Verify SysFont was called for each font configuration
        assert mock_sysfont.call_count == len(ThemeManager.FONTS)
        
        # Verify font cache contains all configured fonts
        for font_name in ThemeManager.FONTS:
            assert font_name in ThemeManager._font_cache
    
    def test_get_color_existing(self):
        """Test getting an existing color from the palette"""
        # Get an existing color
        color = ThemeManager.get_color('background')
        
        # Verify the correct color is returned
        assert color == (0, 128, 0)
    
    def test_get_color_nonexistent(self):
        """Test getting a non-existent color from the palette"""
        # Get a non-existent color
        color = ThemeManager.get_color('nonexistent')
        
        # Verify the default text color is returned
        assert color == ThemeManager.COLORS['text']
    
    def test_get_font_with_initialized_cache(self, reset_font_cache, mock_pygame_font):
        """Test getting a font with initialized cache"""
        _, _, mock_font = mock_pygame_font
        
        # Initialize the font cache
        ThemeManager.initialize()
        
        # Get a font
        font = ThemeManager.get_font('normal')
        
        # Verify the correct font is returned
        assert font is mock_font
    
    def test_get_font_without_initialized_cache(self, reset_font_cache, mock_pygame_font):
        """Test getting a font without initialized cache"""
        mock_init, mock_sysfont, mock_font = mock_pygame_font
        
        # Get a font without prior initialization
        font = ThemeManager.get_font('normal')
        
        # Verify initialization was triggered
        mock_init.assert_called_once()
        
        # Verify the correct font is returned
        assert font is mock_font
    
    def test_get_font_nonexistent(self, reset_font_cache, mock_pygame_font):
        """Test getting a non-existent font"""
        _, _, mock_font = mock_pygame_font
        
        # Initialize the font cache
        ThemeManager.initialize()
        
        # Get a non-existent font
        font = ThemeManager.get_font('nonexistent')
        
        # Verify the default 'normal' font is returned
        assert font is ThemeManager._font_cache['normal']
    
    def test_render_text(self, reset_font_cache, mock_pygame_font):
        """Test rendering text with specified font and color"""
        _, _, mock_font = mock_pygame_font
        
        # Initialize the font cache
        ThemeManager.initialize()
        
        # Render some text
        surface = ThemeManager.render_text("Test Text", "heading", "highlight")
        
        # Verify font.render was called with correct parameters
        mock_font.render.assert_called_once_with("Test Text", True, ThemeManager.COLORS["highlight"])
        
        # Verify the returned surface is the mock surface
        assert surface is mock_font.render.return_value
    
    def test_render_text_default_params(self, reset_font_cache, mock_pygame_font):
        """Test rendering text with default parameters"""
        _, _, mock_font = mock_pygame_font
        
        # Initialize the font cache
        ThemeManager.initialize()
        
        # Render some text with default parameters
        ThemeManager.render_text("Test Text")
        
        # Verify font.render was called with default parameters
        mock_font.render.assert_called_once_with("Test Text", True, ThemeManager.COLORS["text"])
    
    def test_draw_button(self, reset_font_cache, mock_pygame_font):
        """Test drawing a button"""
        _, _, mock_font = mock_pygame_font
        
        # Initialize the font cache
        ThemeManager.initialize()
        
        # Create mocks for required parameters
        mock_surface = MagicMock(spec=pygame.Surface)
        mock_rect = MagicMock(spec=pygame.Rect)
        mock_rect.center = (100, 100)
        
        # Mock render_text to return a surface with a rect
        mock_text_surf = MagicMock(spec=pygame.Surface)
        mock_text_rect = MagicMock(spec=pygame.Rect)
        mock_text_surf.get_rect.return_value = mock_text_rect
        
        # Patch pygame.draw.rect to prevent it from being called with our mock
        with patch('pygame.draw.rect') as mock_draw_rect, \
            patch.object(ThemeManager, 'render_text', return_value=mock_text_surf) as mock_render:
            
            # Draw a button
            ThemeManager.draw_button(mock_surface, mock_rect, "Test Button")
            
            # Verify render_text was called with correct parameters
            mock_render.assert_called_once_with("Test Button", "button", "button_text")
            
            # Verify pygame.draw.rect was called for button background and border
            assert mock_surface.blit.called
            assert mock_draw_rect.call_count == 2
    
    def test_draw_button_hover(self, reset_font_cache, mock_pygame_font):
        """Test drawing a button with hover effect"""
        _, _, mock_font = mock_pygame_font
        
        # Initialize the font cache
        ThemeManager.initialize()
        
        # Create mocks for required parameters
        mock_surface = MagicMock(spec=pygame.Surface)
        mock_rect = MagicMock(spec=pygame.Rect)
        mock_rect.center = (100, 100)
        
        # Mock render_text to return a surface with a rect
        mock_text_surf = MagicMock(spec=pygame.Surface)
        mock_text_rect = MagicMock(spec=pygame.Rect)
        mock_text_surf.get_rect.return_value = mock_text_rect
        
        # Patch pygame.draw.rect to prevent it from being called with our mock
        with patch('pygame.draw.rect') as mock_draw_rect, \
            patch.object(ThemeManager, 'render_text', return_value=mock_text_surf) as mock_render:
            
            # Draw a button with hover effect
            ThemeManager.draw_button(mock_surface, mock_rect, "Test Button", hover=True)
            
            # Verify render_text was called
            mock_render.assert_called_once()
            
            # Verify pygame.draw.rect was called with proper colors
            # First call should use button_hover color
            args1, _ = mock_draw_rect.call_args_list[0]
            assert args1[1] == ThemeManager.COLORS['button_hover']
            
            # Second call should use highlight color for border
            args2, _ = mock_draw_rect.call_args_list[1]
            assert args2[1] == ThemeManager.COLORS['highlight']
    
    def test_draw_button_custom_colors(self, reset_font_cache, mock_pygame_font):
        """Test drawing a button with custom colors"""
        _, _, mock_font = mock_pygame_font
        
        # Initialize the font cache
        ThemeManager.initialize()
        
        # Create mocks for required parameters
        mock_surface = MagicMock(spec=pygame.Surface)
        mock_rect = MagicMock(spec=pygame.Rect)
        mock_rect.center = (100, 100)
        
        # Mock render_text to return a surface with a rect
        mock_text_surf = MagicMock(spec=pygame.Surface)
        mock_text_rect = MagicMock(spec=pygame.Rect)
        mock_text_surf.get_rect.return_value = mock_text_rect
        
        # Patch pygame.draw.rect to prevent it from being called with our mock
        with patch('pygame.draw.rect') as mock_draw_rect, \
            patch.object(ThemeManager, 'render_text', return_value=mock_text_surf) as mock_render:
            
            # Draw a button with custom colors
            ThemeManager.draw_button(
                mock_surface, 
                mock_rect, 
                "Test Button", 
                color_name="button_success", 
                text_color="highlight"
            )
            
            # Verify render_text was called with custom text color
            mock_render.assert_called_once_with("Test Button", "button", "highlight")
            
            # Verify pygame.draw.rect with custom button color
            args, _ = mock_draw_rect.call_args_list[0]
            assert args[1] == ThemeManager.COLORS['button_success']