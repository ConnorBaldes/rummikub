import pygame


class MenuScreen:


    def __init__(self, game):

        self.game = game
        self.screen = pygame.display.set_mode((3400, 2500))

        self.continue_button_img = pygame.image.load("./rummikub/assets/continue_button.png")
        self.continue_button_rect = self.continue_button_img.get_rect(topright=(3350, 2300))

    def handle_events(self, events):

        for event in events: 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.continue_button_rect.collidepoint(event.pos):
                    self.populate_rack()
                    self.save_positions()
                    self.game.change_screen(self.game.game_screen)

    def update(self):
        pass


    def render(self):
        self.screen.fill((0, 128, 0))  # Clear screen

        self.screen.blit(self.continue_button_img, self.continue_button_rect.topleft)

        pygame.display.flip()

    def populate_rack(self) -> None:
        x: int = 35
        y: int = 2015
        for tile in self.game.players[self.game.current_turn].tiles.values():

            if not (x + 75) > 3400:
                tile.set_coordinates(x, y)
                # tile.draw_tile(self.screen)
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

    # Save starting positions at turn start.
    def save_positions(self):
        for tile in self.game.players[self.game.current_turn].tiles.values():
            tile.save_turn_start_position()
            tile.save_pre_drag_pos()
        for tile in self.game.game_screen.board.tiles.values():
            tile.save_turn_start_position()
            tile.save_pre_drag_pos()