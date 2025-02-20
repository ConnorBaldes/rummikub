import pygame
from rummikub.tile import Tile
from rummikub.board import Board
from rummikub.player import Player


class GameScreen:
    def __init__(self, game):

        self.game = game
        self.screen = pygame.display.set_mode((3400, 2500))
        self.board = Board(game)
        self.dragging: Tile = None
        self.offset_x = 0
        self.offset_y = 0

        # Load images
        self.draw_button_img = pygame.image.load("./rummikub/assets/draw_button.png")
        self.end_button_img = pygame.image.load("./rummikub/assets/end_turn_button.png")
        self.player_rack_img = pygame.image.load("./rummikub/assets/rack.png")
        
        # Define positions
        self.draw_button_rect = self.draw_button_img.get_rect(topleft=(50, 1900))
        self.end_button_rect = self.end_button_img.get_rect(topright=(3350, 1900))
        self.player_rack_rect = self.player_rack_img.get_rect(midbottom=(1700, 2500))



    def handle_events(self, events):

        for event in events:

            if event.type == pygame.MOUSEBUTTONDOWN:
                for tile in self.game.players[self.game.current_turn].rack.values():
                    if tile.rect.collidepoint(event.pos):
                        self.dragging = tile
                        self.offset_x = tile.rect.x - event.pos[0]
                        self.offset_y = tile.rect.y - event.pos[1]
                        tile.set_original_coordinates()


                if self.draw_button_rect.collidepoint(event.pos):
                    self.game.players[self.game.current_turn].draw_tile(self.game.deck)
                    self.game.next_turn()
                elif self.end_button_rect.collidepoint(event.pos):
                    if self.board.validate_sets():
                        self.game.next_turn()
                    # TO DO: Reset tiles

            elif event.type == pygame.MOUSEMOTION:
                if self.dragging:
                    self.game.players[self.game.current_turn].rack[self.dragging.get_id()].set_x(event.pos[0] + self.offset_x)
                    self.game.players[self.game.current_turn].rack[self.dragging.get_id()].set_y(event.pos[1] + self.offset_y)
                    print(self.dragging.rect.x)
                    
                    # Prevent movement outside the board
                    self.dragging.set_x(max(0, min(3330, self.dragging.get_x())))
                    self.dragging.set_y(max(0, min(2380, self.dragging.get_y())))

            elif event.type == pygame.MOUSEBUTTONUP:
                if self.dragging:
                    if self.check_overlap(self.dragging):  
                        self.dragging.set_original_coordinates()  # Reset to original position if overlapping
                    else:
                        self.board.update_sets()

                self.dragging = None

    def update(self):
        self.board.update_sets()
    
    def render(self):
        self.screen.fill((0, 128, 0))  # Clear screen
        self.board.draw(self.screen)
        
        # Draw
        self.screen.blit(self.player_rack_img, self.player_rack_rect)
        self.screen.blit(self.draw_button_img, self.draw_button_rect.topleft)
        self.screen.blit(self.end_button_img, self.end_button_rect.topleft)
        self.draw_player_tiles()
        
        pygame.display.update()


    def draw_player_tiles(self) -> None:
        x: int = 35
        y: int = 2015

        if self.dragging:
            self.dragging.draw_tile(self.screen)
        for tile in self.game.players[self.game.current_turn].rack.values():
            if not self.dragging or tile != self.dragging:
                if not (x + 75) > 3400:
                    tile.set_coordinates(x, y)
                    tile.set_original_coordinates()
                    tile.draw_tile(self.screen)
                    if not (x + 220) > 3400:
                        x +=145
                    else:
                        if not (y + 370) > 2500:
                            x = 35
                            y += 245
                        else: 
                            break
                else:
                    if not (y + 370) > 2500:
                        x = 35
                        y += 245
                    else: 
                        break               

    # Function to check if a dragged tile collides with any other tile
    def check_overlap(self, dragged_tile):
        for other_tile in self.board.get_tile_positions():
            if other_tile.id != dragged_tile.id and dragged_tile.rect.colliderect(other_tile.rect):
                return True  # Collision detected
        return False