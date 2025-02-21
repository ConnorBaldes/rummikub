from typing import Type, Tuple, List, Optional
import pygame

class Tile:

    def __init__(self, id: int,  number: int, color: Type[str], image_path: Type[str]):

        self.id = id
        self.number = number
        self.color = color
        self.image: pygame.Surface = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = -1
        self.rect.y = -1
        self.turn_start_pos = (self.rect.x, self.rect.y)  # Saved at turn start
        self.pre_drag_pos = (self.rect.x, self.rect.y) # Saved right before dragging begins
        self.dragging = False
        self.drag_offset = (0, 0)

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

    def draw(self, screen): 
        screen.blit(self.image, self.rect)