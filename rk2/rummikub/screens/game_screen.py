import pygame
from rummikub.tile import Tile
from rummikub.board import Board
from rummikub.player import Player


class GameScreen:
    def __init__(self, game):

        self.game = game
        self.screen = pygame.display.set_mode((3400, 2500))
        self.board = Board(game)
        self.dragging_tile = None

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
                if self.draw_button_rect.collidepoint(event.pos):
                    self.game.players[self.game.current_turn].draw_tile(self.game.deck)
                    self.game.next_turn()
                elif self.end_button_rect.collidepoint(event.pos):
                    if self.board.validate_sets():
                        self.game.next_turn()
                    # TO DO: Reset tiles
            elif event.type == pygame.MOUSEMOTION:
                pass  # Handle tile dragging logic
            elif event.type == pygame.MOUSEBUTTONUP:
                pass  # Handle tile placement logic

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
        
        pygame.display.flip()


    def draw_player_tiles(self) -> None:
        x: int = 35
        y: int = 2015
        for tile in self.game.players[self.game.current_turn].rack:
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

            