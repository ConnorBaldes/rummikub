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
                    self.game.change_screen(self.game.game_screen)

    def update(self):
        pass


    def render(self):
        self.screen.fill((0, 128, 0))  # Clear screen

        self.screen.blit(self.continue_button_img, self.continue_button_rect.topleft)

        pygame.display.flip()