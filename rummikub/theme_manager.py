import pygame
from typing import Dict, Tuple, Optional

class ThemeManager:
    """Manages consistent UI theming across the Rummikub game."""
    
    # Color palette
    COLORS = {
        'background': (0, 128, 0),      # Green table
        'text': (255, 255, 255),        # White text
        'highlight': (255, 255, 0),     # Yellow highlight
        'button': (50, 50, 50),         # Dark gray button
        'button_hover': (75, 75, 75),   # Lighter gray on hover
        'button_text': (255, 255, 255), # White button text
        'button_success': (50, 200, 50), # Green success button
        'button_danger': (200, 50, 50),  # Red danger button
        'button_info': (50, 100, 200),   # Blue info button (new)
        'tile_border': (0, 0, 0),       # Black border
        'valid': (0, 255, 0, 128),      # Green translucent overlay
        'invalid': (255, 0, 0, 128),    # Red translucent overlay
        'board_area': (0, 100, 0),      # Darker green for board area
        'rack_area': (139, 69, 19),     # Brown for rack
    }
    
    # Font configurations
    FONTS = {
        'title': {'size': 60, 'bold': True},
        'heading': {'size': 50, 'bold': True},
        'normal': {'size': 36, 'bold': False},
        'small': {'size': 28, 'bold': False},
        'button': {'size': 35, 'bold': True},
    }
    
    # Cached font objects
    _font_cache: Dict[str, pygame.font.Font] = {}
    
    @classmethod
    def initialize(cls):
        """Initialize pygame font module and create cached fonts."""
        pygame.font.init()
        
        # Generate font cache
        for font_name, font_config in cls.FONTS.items():
            cls._font_cache[font_name] = pygame.font.SysFont(
                'Arial', 
                font_config['size'], 
                bold=font_config.get('bold', False)
            )
    
    @classmethod
    def get_color(cls, color_name: str) -> Tuple[int, ...]:
        """Get a color by name from the color palette."""
        return cls.COLORS.get(color_name, cls.COLORS['text'])
    
    @classmethod
    def get_font(cls, font_name: str) -> pygame.font.Font:
        """Get a font by name from the font cache."""
        if not cls._font_cache:
            cls.initialize()
        return cls._font_cache.get(font_name, cls._font_cache['normal'])
    
    @classmethod
    def render_text(cls, text: str, font_name: str = 'normal', color_name: str = 'text') -> pygame.Surface:
        """Render text with specified font and color."""
        font = cls.get_font(font_name)
        color = cls.get_color(color_name)
        return font.render(text, True, color)
    
    @classmethod
    def draw_button(cls, surface: pygame.Surface, rect: pygame.Rect, text: str, 
                   color_name: str = 'button', text_color: str = 'button_text',
                   hover: bool = False) -> None:
        """Draw a themed button on the given surface."""
        # Draw button background
        bg_color = cls.get_color('button_hover' if hover else color_name)
        pygame.draw.rect(surface, bg_color, rect, border_radius=10)
        
        # Draw button border
        border_color = cls.get_color('highlight' if hover else 'tile_border')
        pygame.draw.rect(surface, border_color, rect, width=2, border_radius=10)
        
        # Draw button text
        text_surf = cls.render_text(text, 'button', text_color)
        text_rect = text_surf.get_rect(center=rect.center)
        surface.blit(text_surf, text_rect)