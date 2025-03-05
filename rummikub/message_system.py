# message_system.py
import pygame
from typing import List, Tuple, Optional
import time
from rummikub.theme_manager import ThemeManager

class Message:
    """Represents a game message with fade-in/fade-out effects."""
    
    def __init__(self, text: str, duration: float = 3.0, color_name: str = 'text',
                font_name: str = 'normal', position: Tuple[int, int] = None):
        self.text = text
        self.duration = duration
        self.color_name = color_name
        self.font_name = font_name
        self.position = position
        self.creation_time = time.time()
        self.alpha = 0  # Start fully transparent
        self.fade_in_duration = 0.3
        self.fade_out_duration = 0.5
    
    def update(self) -> bool:
        """Update message alpha based on its lifetime. Returns False when expired."""
        current_time = time.time()
        elapsed = current_time - self.creation_time
        
        # Handle fade-in
        if elapsed < self.fade_in_duration:
            self.alpha = int(255 * (elapsed / self.fade_in_duration))
        # Handle fade-out
        elif elapsed > (self.duration - self.fade_out_duration):
            remaining = self.duration - elapsed
            self.alpha = int(255 * (remaining / self.fade_out_duration))
        # Fully visible
        else:
            self.alpha = 255
            
        # Check if message has expired
        return elapsed < self.duration
    
    def draw(self, surface: pygame.Surface, default_y: int = 100) -> None:
        """Draw the message with the current alpha value."""
        font = ThemeManager.get_font(self.font_name)
        color = ThemeManager.get_color(self.color_name)
        
        # Create a text surface with the current alpha
        text_surf = font.render(self.text, True, color)
        text_surf.set_alpha(self.alpha)
        
        # Position the message
        if self.position:
            x, y = self.position
        else:
            x = surface.get_width() // 2 - text_surf.get_width() // 2
            y = default_y
            
        surface.blit(text_surf, (x, y))

class MessageSystem:
    """Manages game messages and notifications."""
    
    def __init__(self):
        self.messages: List[Message] = []
        self.max_messages = 3
        self.vertical_spacing = 50
    
    def add_message(self, text: str, duration: float = 3.0, color_name: str = 'text',
                   font_name: str = 'normal', position: Tuple[int, int] = None) -> None:
        """Add a new message to the system."""
        self.messages.append(Message(text, duration, color_name, font_name, position))
        
        # Trim excess messages
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)
    
    def update(self) -> None:
        """Update all active messages, removing expired ones."""
        self.messages = [msg for msg in self.messages if msg.update()]
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw all active messages to the screen."""
        for i, message in enumerate(self.messages):
            y_pos = 100 + i * self.vertical_spacing
            message.draw(surface, default_y=y_pos)
    
    def clear(self) -> None:
        """Clear all messages."""
        self.messages.clear()