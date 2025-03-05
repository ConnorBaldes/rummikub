# Updated sections for tile.py
from typing import Type, Tuple, List, Optional
import pygame
from rummikub.theme_manager import ThemeManager

class Tile:
    """
    Represents a tile in the Rummikub game.
    
    Each tile has a numeric value, color, and image representation.
    Tiles can be dragged, dropped, and highlighted based on game state.
    
    Attributes:
        id (int): Unique identifier for the tile
        number (int): Numeric value of the tile (1-13)
        color (str): Color of the tile ('red', 'blue', 'black', 'orange')
        is_joker (bool): Whether this tile is a joker
        image (pygame.Surface): Visual representation of the tile
        rect (pygame.Rect): Rectangle representing the tile's position and size
        dragging (bool): Whether the tile is currently being dragged
        highlight (bool): Whether the tile should be visually highlighted
        highlight_color (str): Name of the highlight color from ThemeManager
    """

    # Default tile dimensions
    DEFAULT_WIDTH = 130
    DEFAULT_HEIGHT = 200

    def __init__(self, id: int, number: int, color: Type[str], image_path: Type[str], is_joker: bool = False,
                 width: int = None, height: int = None):
        """
        Initialize a new tile.
        
        Args:
            id (int): Unique identifier for the tile
            number (int): Numeric value of the tile (1-13)
            color (str): Color of the tile ('red', 'blue', 'black', 'orange')
            image_path (str): Path to the tile's image file
            is_joker (bool, optional): Whether this tile is a joker. Defaults to False.
            width (int, optional): Custom width for the tile. Defaults to DEFAULT_WIDTH.
            height (int, optional): Custom height for the tile. Defaults to DEFAULT_HEIGHT.
        """
        self.id = id
        self.number = number
        self.color = color
        self.is_joker = is_joker
        self.in_set = False  # Track if the joker is currently in a set
        
        # Load the original image
        self.original_image = pygame.image.load(image_path)
        
        # Set dimensions (use defaults if not specified)
        self.width = width if width is not None else self.DEFAULT_WIDTH
        self.height = height if height is not None else self.DEFAULT_HEIGHT
        
        # Resize the image to the specified dimensions
        self.image = self.resize_image(self.width, self.height)
        
        # Initialize position and state
        self.rect = self.image.get_rect()
        self.rect.x = -1
        self.rect.y = -1
        self.turn_start_pos = (self.rect.x, self.rect.y)  # Saved at turn start
        self.pre_drag_pos = (self.rect.x, self.rect.y)  # Saved right before dragging begins
        self.dragging = False
        self.drag_offset = (0, 0)
        self.highlight = False
        self.highlight_color = None
        self.scale_factor = 1.0  # For hover/drag animation

    def resize_image(self, width: int, height: int) -> pygame.Surface:
        """
        Resize the tile image to the specified dimensions.
        
        Args:
            width (int): Target width
            height (int): Target height
            
        Returns:
            pygame.Surface: The resized image
        """
        return pygame.transform.smoothscale(self.original_image, (width, height))

    def set_size(self, width: int, height: int) -> None:
        """
        Set new dimensions for the tile and resize its image.
        
        Args:
            width (int): New width for the tile
            height (int): New height for the tile
        """
        # Store the old center position to maintain positioning
        old_center = self.rect.center
        
        # Update dimensions
        self.width = width
        self.height = height
        
        # Resize the image
        self.image = self.resize_image(width, height)
        
        # Update the rect and maintain position
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def set_highlight(self, highlight: bool, color_name: str = None) -> None:
        """
        Set the highlight state of the tile.
        
        Args:
            highlight (bool): Whether to highlight the tile
            color_name (str, optional): Color name from ThemeManager. Defaults to None.
        """
        self.highlight = highlight
        self.highlight_color = color_name

    def draw(self, screen): 
        """
        Draw the tile with highlight effects if active.
        
        Args:
            screen: The pygame surface to draw on
        """
        # Scale the image if dragging
        current_image = self.image
        
        if self.dragging:
            # Create a larger version while dragging
            scale = 1.1  # 10% larger
            scaled_width = int(self.width * scale)
            scaled_height = int(self.height * scale)
            current_image = self.resize_image(scaled_width, scaled_height)
            
            # Adjust rect to maintain the same position
            offset_x = (scaled_width - self.rect.width) // 2
            offset_y = (scaled_height - self.rect.height) // 2
            draw_rect = pygame.Rect(self.rect.x - offset_x, self.rect.y - offset_y, 
                                    scaled_width, scaled_height)
        else:
            draw_rect = self.rect
            
        # Draw the tile image
        screen.blit(current_image, draw_rect)
        
        # Draw highlight if active
        if self.highlight and self.highlight_color:
            highlight_surface = pygame.Surface((draw_rect.width, draw_rect.height), pygame.SRCALPHA)
            highlight_color = ThemeManager.get_color(self.highlight_color)
            highlight_surface.fill(highlight_color)
            screen.blit(highlight_surface, draw_rect)

    def get_id(self) -> int:
        return self.id

    def get_number(self) -> int:
        return self.number
    
    def get_color(self) -> Type[str]:
        return self.color
    
    def get_image(self) -> pygame.Surface:
        return self.image
    
    def get_x(self) -> Optional[int]:
        return self.rect.x
    
    def get_y(self) -> Optional[int]:
        return self.rect.y
    
    def get_coordinates(self) -> Tuple[int, int]:
        return (self.rect.x, self.rect.y)
    
    def get_size(self) -> Tuple[int, int]:
        """
        Get the current dimensions of the tile.
        
        Returns:
            Tuple[int, int]: Width and height of the tile
        """
        return (self.width, self.height)

    def set_x(self, x) -> None:
        self.rect.x = x

    def set_y(self, y) -> None:
        self.rect.y = y

    def set_coordinates(self, x, y) -> None:
        self.rect.x = x
        self.rect.y = y
    
    def get_pre_drag_pos(self) -> Tuple[int, int]:
        return self.pre_drag_pos

    def save_pre_drag_pos(self) -> None:
         self.pre_drag_pos = self.get_coordinates()
    
    def save_turn_start_position(self) -> None:
        self.turn_start_pos = self.get_coordinates()

    def start_drag(self, mouse_pos) -> None:
        self.dragging = True
        # Save tiles pre-drag position
        self.pre_drag_pos = self.get_coordinates()
        self.drag_offset = (self.rect.x - mouse_pos[0], self.rect.y - mouse_pos[1])

    def update_drag(self, mouse_pos) -> None:
        if self.dragging:
            self.set_coordinates(
                mouse_pos[0] + self.drag_offset[0],
                mouse_pos[1] + self.drag_offset[1]
            )
    
    def stop_drag(self) -> None:
        self.dragging = False

    def revert_to_pre_drag(self) -> None:
        self.set_coordinates(self.pre_drag_pos[0], self.pre_drag_pos[1])

    def revert_to_turn_start(self) -> None:
        self.set_coordinates(self.turn_start_pos[0], self.turn_start_pos[1])

    def reset_joker(self) -> None:
        """Reset a joker tile back to its original state."""
        if self.is_joker:
            self.number = 0  # Reset to 0
            self.in_set = False   