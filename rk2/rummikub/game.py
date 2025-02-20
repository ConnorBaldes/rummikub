import pygame
from rummikub.player import Player
from rummikub.deck import Deck
from rummikub.screens.game_screen import GameScreen
from rummikub.screens.menu import MenuScreen

def get_player_names():
    while True:
        names = input("Enter player names (comma-separated, 2-4 players): ").split(',')
        names = [name.strip() for name in names if name.strip()]
        if 2 <= len(names) <= 4:
            return names
        print("Invalid input. Please enter between 2 and 4 names.")

class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((3400, 2500))
        pygame.display.set_caption("Rummikub")
        self.clock = pygame.time.Clock()
        self.running = True
        self.deck = Deck("./rummikub/assets/tiles")
        self.players = [Player(name, self.deck.assign_tiles()) for name in self._get_player_names()]
        self.current_turn = 0
        self.game_screen = GameScreen(self)
        self.menu_screen = MenuScreen(self)
        self.current_screen = self.menu_screen
    
    def _get_player_names(self):
        while True:
            names = input("Enter player names (comma-separated, 2-4 players): ").split(',')
            names = [name.strip() for name in names if name.strip()]
            if 2 <= len(names) <= 4:
                return names
            print("Invalid input. Please enter between 2 and 4 names.")
    
    def change_screen(self, new_screen):
        self.current_screen = new_screen
    
    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
        self.current_screen.handle_events(events)
    
    def update(self):
        self.current_screen.update()
    
    def render(self):
        self.current_screen.render()
        pygame.display.flip()
    
    def next_turn(self):
        self.current_turn = (self.current_turn + 1) % len(self.players)
        self.change_screen(self.menu_screen)
        print(f"{self.players[self.current_turn].name}'s turn")
    
    def run(self):

        while self.running:
            self.handle_events()
            self.update()
            self.render()  # Green background
            if not self.running:
                break
            