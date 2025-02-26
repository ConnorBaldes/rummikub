import pygame
from rummikub.player import Player
from rummikub.deck import Deck
from rummikub.screens.game_screen import GameScreen
from rummikub.screens.menu import SetupMenu, TurnMenu

class Game:
    def __init__(self):
        self.deck = Deck("./rummikub/assets/tiles")
        pygame.init()
        self.screen = pygame.display.set_mode((3400, 2500))
        pygame.display.set_caption("Rummikub")
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_turn = 0
        self.players = []  # Will be set after name submission

        # Use our new SetupMenu for initial configuration.
        self.menu_screen = SetupMenu(self)
        self.current_screen = self.menu_screen

        self.game_screen = GameScreen(self)

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
        if self.current_screen != self.game_screen:
            self.current_screen.draw(self.screen)
            pygame.display.flip()
        else:
            self.current_screen.render()

    def populate_rack(self):
        """Places the current player's tiles in a neatly formatted rack layout."""
        left_margin = 35
        top_margin = 2015
        right_margin = 35  # Margin on the right side
        gap = 20           # Space between tiles

        current_player = self.players[self.current_turn]
        if not current_player.tiles:
            return

        # Get tile dimensions from the first tile.
        sample_tile = next(iter(current_player.tiles.values()))
        tile_width = sample_tile.image.get_width()
        tile_height = sample_tile.image.get_height()

        # Compute available width and max number of columns.
        screen_width = self.screen.get_width()
        available_width = screen_width - left_margin - right_margin
        num_columns = max(1, available_width // (tile_width + gap))

        # Arrange tiles in a grid pattern.
        for idx, tile in enumerate(current_player.tiles.values()):
            row = idx // num_columns
            col = idx % num_columns
            x = left_margin + col * (tile_width + gap)
            y = top_margin + row * (tile_height + gap)
            tile.set_coordinates(x, y)

    def save_positions(self):
        """Saves the starting positions of all tiles before a turn begins."""
        for tile in self.players[self.current_turn].tiles.values():
            tile.save_turn_start_position()
            tile.save_pre_drag_pos()
        for tile in self.game_screen.board.tiles.values():
            tile.save_turn_start_position()
            tile.save_pre_drag_pos()

    def next_turn(self):
        """Advances to the next player's turn and updates the turn menu."""
        self.current_turn = (self.current_turn + 1) % len(self.players)
        turn_message = f"{self.players[self.current_turn].name}, press Continue to play your turn."

        # Populate rack and save positions before switching screens.
        self.populate_rack()
        self.save_positions()

        self.change_screen(TurnMenu(self, turn_message))
        print(f"{self.players[self.current_turn].name}'s turn")

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()

