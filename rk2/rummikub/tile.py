from typing import Type, Tuple, List, Optional
import pygame

class Tile:

    def __init__(self, id: int,  number: int, color: Type[str], image_path: Type[str]):

        self.id = id
        self.number = number
        self.color = color
        self.image: pygame.Surface = pygame.image.load(image_path)
        self.rect.x = None
        self.rect.y = None

    def __repr__(self) -> str:
        return f'({self.id})'
    
    def __string__(self) -> str:
        return f'({self.id}, {self.number}, {self.color})'
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Tile):
            raise TypeError(f"Cannot compare Tile with {type(other).__name__}")
        return self.id == other.get_id()
    
    def __ne__(self, other) -> bool:
        if not isinstance(other, Tile):
            raise TypeError(f"Cannot compare Tile with {type(other).__name__}")
        return self.id != other.get_id()
    
    def __lt__(self, other) -> bool:
        if not isinstance(other, Tile):
            raise TypeError(f"Cannot compare Tile with {type(other).__name__}")
        return self.number < other.get_number()
        
    def __le__(self, other) -> bool:
        if not isinstance(other, Tile):
            raise TypeError(f"Cannot compare Tile with {type(other).__name__}")
        return self.number <= other.get_number()
    
    def __gt__(self, other) -> bool:
        if not isinstance(other, Tile):
            raise TypeError(f"Cannot compare Tile with {type(other).__name__}")    
        return self.number > other.get_number()
   
    def __ge__(self, other) -> bool:    
        if not isinstance(other, Tile):
            raise TypeError(f"Cannot compare Tile with {type(other).__name__}")   
        return self.number >= other.get_number()
 
    def __radd__(self, other) -> int:
        if not isinstance(other, int):
            raise TypeError(f"Cannot add Tile number to {type(other).__name__}")    
        return other + self.number

    def __rsub__(self, other) -> int:
        if not isinstance(other, int):
            raise TypeError(f"Cannot subtract Tile number from {type(other).__name__}")    
        return other - self.number


    def get_id(self) -> int:
        return str(self.id)

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
        return (self.x, self.y)
    

    def set_x(self, x) -> None:
        self.rect.x = x

    def set_y(self, y) -> None:
        self.rect.y = y

    def set_coordinates(self, x, y) -> None:
        self.rect.x = x
        self.rect.y = y


    def draw_tile(self, screen) -> None:
        screen.blit(self.image, self.rect)