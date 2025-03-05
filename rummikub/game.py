# Updated sections for game.py
import pygame
from rummikub.player import Player
from rummikub.deck import Deck
from rummikub.screens.game_screen import GameScreen
from rummikub.screens.menu import SetupMenu, TurnMenu

class Game:
    """
    Main game controller that manages game state, players, and screens.
    
    This class handles the overall game flow, screen transitions, and game rules.
    """
    
    def __init__(self):
        """Initialize the game with default settings."""
        self.deck = Deck("./rummikub/assets/tiles_2")
        pygame.init()
        self.screen = pygame.display.set_mode((3400, 2500))
        pygame.display.set_caption("Rummikub")
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_turn = 0
        self.players = []  # Will be set after name submission
        
        # Add game state tracking
        self.game_over = False
        self.winner = None
        
        # Add statistics tracking
        self.statistics = {
            'turns_played': 0,
            'tiles_drawn': 0,
            'valid_sets_formed': 0,
            'invalid_moves': 0
        }

        # Use our SetupMenu for initial configuration
        self.menu_screen = SetupMenu(self)
        self.current_screen = self.menu_screen

        self.game_screen = GameScreen(self)

    def change_screen(self, new_screen):
        """Change the active screen."""
        self.current_screen = new_screen

    def handle_events(self):
        """Process game events."""
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
        self.current_screen.handle_events(events)

    def update(self):
        """Update game state."""
        self.current_screen.update()

    def render(self):
        """Render the current screen."""
        if self.current_screen != self.game_screen:
            self.current_screen.draw(self.screen)
            pygame.display.flip()
        else:
            self.current_screen.render()

    def populate_rack(self):
        """Place the current player's tiles in a neatly formatted rack layout."""
        left_margin = 35
        top_margin = 2015
        right_margin = 35  # Margin on the right side
        gap = 20           # Space between tiles

        current_player = self.players[self.current_turn]
        if not current_player.tiles:
            return

        # Get tile dimensions from the first tile
        sample_tile = next(iter(current_player.tiles.values()))
        tile_width = sample_tile.image.get_width()
        tile_height = sample_tile.image.get_height()

        # Compute available width and max number of columns
        screen_width = self.screen.get_width()
        available_width = screen_width - left_margin - right_margin
        num_columns = max(1, available_width // (tile_width + gap))

        # Arrange tiles in a grid pattern
        for idx, tile in enumerate(current_player.tiles.values()):
            row = idx // num_columns
            col = idx % num_columns
            x = left_margin + col * (tile_width + gap)
            y = top_margin + row * (tile_height + gap)
            tile.set_coordinates(x, y)

    def save_positions(self):
        """Save the starting positions of all tiles before a turn begins."""
        for tile in self.players[self.current_turn].tiles.values():
            tile.save_turn_start_position()
            tile.save_pre_drag_pos()
        for tile in self.game_screen.board.tiles.values():
            tile.save_turn_start_position()
            tile.save_pre_drag_pos()

    def next_turn(self):
        """Advance to the next player's turn and update the turn menu."""
        self.current_turn = (self.current_turn + 1) % len(self.players)
        self.statistics['turns_played'] += 1
        
        turn_message = f"{self.players[self.current_turn].name}"
        
        # Create statistics message
        stats_message = (f"Game Statistics: {self.statistics['turns_played']} turns played, "
                        f"{self.statistics['tiles_drawn']} tiles drawn, "
                        f"{len(self.deck)} tiles remaining in deck")

        # Populate rack and save positions before switching screens
        self.populate_rack()
        self.save_positions()

        self.change_screen(TurnMenu(self, turn_message, stats_message))
        print(f"{self.players[self.current_turn].name}'s turn")

    # Keep other methods, but enhance with statistics tracking where relevant
    
    def validate_turn(self) -> bool:
        """Validate the current player's turn."""
        if len(self.game_screen.board.added_tiles) > 0:
            if self.check_initial_meld():
                if self.game_screen.board.validate_sets():
                    self.statistics['valid_sets_formed'] += 1
                    return True
        else:
            print('No tiles played.')
        
        self.statistics['invalid_moves'] += 1
        return False


    def check_initial_meld(self) -> bool:
        """
        Checks if the current player has met their initial meld requirement.
        For the initial meld, the sum of tile values played from the player's rack (this turn)
        must be at least 30 points.
        
        Returns True if the initial meld requirement is met (or was met previously),
        otherwise returns False.
        """
        current_player = self.players[self.current_turn]
        
        # If the player already met their initial meld in a previous turn, print and return True.
        if current_player.initial_meld:
            print("Initial meld already met in a previous turn.")
            return True
        
        # Calculate the total value of the tiles played this turn.
        total_value = 0
        for tile_id in self.game_screen.board.added_tiles:
            tile = self.game_screen.board.tiles.get(tile_id)
            if tile:
                total_value += tile.get_number()
        
        # Check if the total meets the 30 point requirement.
        if total_value >= 30:
            current_player.initial_meld = True
            print(f"Initial meld met this turn with a total value of {total_value}.")
            return True
        else:
            print(f"Initial meld not met. Current total value is {total_value}.")
            return False
        

    def check_for_win(self) -> bool:
        """
        Checks if the current player has any tiles left in their tile list.
        
        Returns:
            True if the current player has no tiles left (winning the game), otherwise False.
        """
        current_player = self.players[self.current_turn]
        if len(current_player.tiles) == 0:
            print(f"Player {current_player.name} has no tiles left and wins the game!")
            self.game_over = True
            self.winner = current_player.name
            
            # Return to setup menu with win message
            win_message = f"{current_player.name} wins the game with {self.statistics['turns_played']} turns played!"
            self.menu_screen = SetupMenu(self, win_message)
            self.change_screen(self.menu_screen)
            return True
        else:
            print(f"Player {current_player.name} still has {len(current_player.tiles)} tiles left.")
            return False



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

