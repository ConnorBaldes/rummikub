import os
import pygame
import pygame_menu
from pygame_menu import themes, BaseImage
import random
from rummikub.player import Player
from rummikub.deck import Deck

class SetupMenu:
    """
    Initial game setup and home screen with comprehensive game information 
    and visual examples of gameplay elements.
    """

    def __init__(self, game, end_message=None):
        self.game = game
        self.current_page = "MAIN"  # Track which page we're viewing
        
        # Define a custom theme with the game's color scheme
        custom_theme = themes.THEME_DARK.copy()
        custom_theme.background_color = (0, 100, 50)  # Richer green background
        custom_theme.title_font_size = 60
        custom_theme.widget_font_size = 36
        custom_theme.widget_font_color = (255, 255, 255)
        
        # Create the main menu
        self.menu = pygame_menu.Menu(
            title="Rummikub",
            height=game.screen.get_height(),
            width=game.screen.get_width(),
            theme=custom_theme
        )
        
        # Store references to different "pages" (menus)
        self.menus = {
            "MAIN": self.menu,
            "RULES": self._create_rules_menu(),
            "EXAMPLES": self._create_examples_menu(),
            "SETUP": self._create_setup_menu()
        }
        
        # Initialize the main menu
        self._setup_main_menu(end_message)
        
        # Set initial menu based on context
        if end_message:
            self.current_page = "SETUP"
            self.menu = self.menus["SETUP"]

    def _setup_main_menu(self, end_message=None):
        """Set up the main menu with banner and navigation buttons."""
        self.menu.clear()
        
        # Add the banner at the top
        banner_path = "./rummikub/assets/banner.png"
        if os.path.exists(banner_path):
            banner = BaseImage(banner_path)
            banner_scaled = banner.resize(width=int(self.game.screen.get_width() * 0.8), 
                                          height=int(self.game.screen.get_height() * 0.15))
            self.menu.add.image(banner_scaled, margin=(0, 20))
        else:
            self.menu.add.label("RUMMIKUB", font_size=80, font_color=(255, 215, 0))
        
        # If we have an end message (from a completed game), display it
        if end_message:
            self.menu.add.label(end_message, font_size=50, font_color=(255, 255, 0))
            self.menu.add.vertical_margin(10)
        
        # Add navigation buttons
        self.menu.add.button("Game Rules", self._show_rules, font_size=45, background_color=(30, 80, 30))
        self.menu.add.vertical_margin(10)
        self.menu.add.button("Game Examples", self._show_examples, font_size=45, background_color=(30, 80, 30))
        self.menu.add.vertical_margin(10)
        self.menu.add.button("Start Game", self._show_setup, font_size=45, background_color=(40, 150, 40))
        self.menu.add.vertical_margin(10)
        self.menu.add.button("Quit", pygame_menu.events.EXIT, font_size=45, background_color=(150, 40, 40))

    def _create_rules_menu(self):
        """Create the rules page."""
        rules_menu = pygame_menu.Menu(
            title="Game Rules",
            height=self.game.screen.get_height(),
            width=self.game.screen.get_width(),
            theme=self.menu.get_theme()
        )
        
        # Game Objective
        rules_menu.add.label("Game Objective", font_size=45, font_color=(255, 215, 0))
        rules_menu.add.label(
            "Be the first player to play all the tiles from your rack by forming them into valid sets.",
            font_size=32,
            max_char=80,
            margin=(0, 10)
        )
        rules_menu.add.vertical_margin(20)
        
        # Core Rules
        rules_menu.add.label("Core Rules", font_size=45, font_color=(255, 215, 0))
        
        rules = [
            "• To start, each player draws 14 tiles and arranges them on their rack.",
            "• On each turn, players must place tiles on the board in valid sets or manipulate existing sets.",
            "• Valid sets include: GROUPS (same number, different colors) or RUNS (consecutive numbers, same color).",
            "• Initial meld must total at least 30 points using tiles from your rack.",
            "• If a player cannot play, they must draw a tile and their turn ends.",
            "• The first player to empty their rack wins the game!"
        ]
        
        for rule in rules:
            rules_menu.add.label(rule, font_size=32, max_char=100)
        
        rules_menu.add.vertical_margin(30)
        rules_menu.add.button("Back to Main Menu", self._show_main, font_size=40, background_color=(30, 80, 30))
        
        return rules_menu

    def _create_examples_menu(self):
        """Create the examples page."""
        examples_menu = pygame_menu.Menu(
            title="Game Examples",
            height=self.game.screen.get_height(),
            width=self.game.screen.get_width(),
            theme=self.menu.get_theme()
        )
        
        examples_menu.add.label("Examples of Valid Sets", font_size=45, font_color=(255, 215, 0))
        
        # Example 1: Group (same number, different colors)
        examples_menu.add.vertical_margin(20)
        examples_menu.add.label("Group Example: Same number, different colors", font_size=32)
        self._add_tile_row(examples_menu, ["tile_8_red.png", "tile_8_blue.png", "tile_8_black.png", "tile_8_orange.png"])
        
        # Example 2: Run (consecutive numbers, same color)
        examples_menu.add.vertical_margin(20)
        examples_menu.add.label("Run Example: Consecutive numbers, same color", font_size=32)
        self._add_tile_row(examples_menu, ["tile_4_blue.png", "tile_5_blue.png", "tile_6_blue.png", "tile_7_blue.png"])
        
        # Example 3: Joker example
        examples_menu.add.vertical_margin(20)
        examples_menu.add.label("Joker Example: Joker substituting for a missing tile", font_size=32)
        self._add_tile_row(examples_menu, ["tile_2_red.png", "tile_3_red.png", "tile_joker_1.png", "tile_5_red.png"])
        
        examples_menu.add.vertical_margin(20)
        examples_menu.add.label("Manipulating Tiles", font_size=45, font_color=(255, 215, 0))
        
        manipulation_text = [
            "• You can rearrange tiles on the board as long as all sets remain valid after your turn.",
            "• Add tiles from your rack to existing sets.",
            "• Split runs to create new sets.",
            "• Move tiles between sets to create new combinations.",
            "• Jokers can substitute for any tile and can be retrieved by replacing them."
        ]
        
        for text in manipulation_text:
            examples_menu.add.label(text, font_size=32, max_char=100)
        
        examples_menu.add.vertical_margin(30)
        examples_menu.add.button("Back to Main Menu", self._show_main, font_size=40, background_color=(30, 80, 30))
        
        return examples_menu

    def _create_setup_menu(self):
        """Create the setup page."""
        setup_menu = pygame_menu.Menu(
            title="Player Setup",
            height=self.game.screen.get_height(),
            width=self.game.screen.get_width(),
            theme=self.menu.get_theme()
        )
        
        setup_menu.add.label("Player Setup", font_size=45, font_color=(255, 215, 0))
        setup_menu.add.vertical_margin(20)
        
        setup_menu.add.label("Enter 2-4 player names, separated by commas:", font_size=36)
        self.name_input = setup_menu.add.text_input(
            title='',
            default="Connor, Elsa",
            maxchar=100,
            textinput_id="name_input",
            # cursor_color=(255, 255, 255),
            background_color=(30, 70, 40),
            font_size=36
        )
        
        setup_menu.add.vertical_margin(30)
        setup_menu.add.button("Start Game", self.submit_names, font_size=45, background_color=(40, 150, 40))
        setup_menu.add.vertical_margin(10)
        setup_menu.add.button("Back to Main Menu", self._show_main, font_size=40, background_color=(30, 80, 30))
        
        return setup_menu

    def _add_tile_row(self, menu, tile_filenames):
        """Add a horizontal row of tile images to the menu."""
        tile_width, tile_height = 100, 150  # Reduced size for display in menu
        
        # Create a surface to hold the tile row
        total_width = (tile_width + 10) * len(tile_filenames)
        surface = pygame.Surface((total_width, tile_height), pygame.SRCALPHA)
        
        # Add tiles to the surface
        for i, filename in enumerate(tile_filenames):
            tile_path = os.path.join("./rummikub/assets/tiles_2/", filename)
            if os.path.exists(tile_path):
                image = pygame.image.load(tile_path)
                scaled_image = pygame.transform.scale(image, (tile_width, tile_height))
                surface.blit(scaled_image, (i * (tile_width + 10), 0))
        
        # Save the surface as a temporary image
        temp_file = "./rummikub/assets/tiles_2/temp_row.png"
        pygame.image.save(surface, temp_file)
        
        # Add the image to the menu
        tile_row = BaseImage(temp_file)
        menu.add.image(tile_row)

    def _show_main(self):
        """Show the main menu."""
        self.current_page = "MAIN"
        self.menu = self.menus["MAIN"]

    def _show_rules(self):
        """Show the rules page."""
        self.current_page = "RULES"
        self.menu = self.menus["RULES"]

    def _show_examples(self):
        """Show the examples page."""
        self.current_page = "EXAMPLES"
        self.menu = self.menus["EXAMPLES"]

    def _show_setup(self):
        """Show the setup page."""
        self.current_page = "SETUP"
        self.menu = self.menus["SETUP"]

    def submit_names(self):
        """Process submitted player names and start the game."""
        names = [name.strip() for name in self.name_input.get_value().split(",") if name.strip()]
        
        if 2 <= len(names) <= 4:
            # Reset the game state
            self.game.deck = Deck("./rummikub/assets/tiles_2")
            self.game.players = [Player(self.game, name) for name in names]
            self.game.current_turn = 0
            self.game.game_over = False
            self.game.winner = None
            
            # Reset statistics
            self.game.statistics = {
                'turns_played': 0,
                'tiles_drawn': 0,
                'valid_sets_formed': 0,
                'invalid_moves': 0
            }
            
            # Prepare the player rack and move to the first turn
            self.game.populate_rack()
            self.game.save_positions()
            
            # Transition to the first player's turn menu
            turn_message = f"{self.game.players[self.game.current_turn].name}"
            self.game.change_screen(TurnMenu(self.game, turn_message))
        else:
            # Add error message to setup menu
            self.menus["SETUP"].add.label(
                "Please enter 2 to 4 player names, separated by commas.",
                font_color=(255, 100, 100),
                font_size=36
            )

    def handle_events(self, events):
        """Handle menu events."""
        self.menu.update(events)

    def update(self):
        pass

    def draw(self, surface):
        """Draw the current menu."""
        self.menu.draw(surface)


class TurnMenu:
    """Displays the current player's turn in a clean, elegant manner."""

    def __init__(self, game, turn_message, stats_message=None):
        self.game = game
        self.turn_message = turn_message
        self.stats_message = stats_message

        # Create a simpler theme
        custom_theme = themes.THEME_DARK.copy()
        custom_theme.background_color = (0, 70, 30, 230)  # Semi-transparent dark green
        custom_theme.title_font_size = 50
        custom_theme.widget_font_size = 36
        custom_theme.widget_font_color = (220, 220, 220)
        custom_theme.title_background_color = (0, 80, 0)
        custom_theme.title_font_color = (255, 230, 150)
        custom_theme.selection_color = (200, 200, 100)
        custom_theme.widget_margin = (0, 15)
        
        # Create menu with appropriate size
        width = game.screen.get_width() - 200
        height = game.screen.get_height() - 200
        
        self.menu = pygame_menu.Menu(
            title="Player Turn",
            width=width,
            height=height,
            theme=custom_theme,
            center_content=True,
            columns=1
        )
        
        # Build clean, simple interface
        self.create_turn_display()
        self.create_tip()
        self.create_continue_button()
        
    def create_turn_display(self):
        """Create a simple, elegant turn display."""
        self.menu.add.vertical_margin(30)
        
        # Next player heading
        self.menu.add.label(
            "NEXT PLAYER",
            font_size=40,
            font_color=(200, 230, 200)
        )
        
        self.menu.add.vertical_margin(20)
        
        # Player name
        self.menu.add.label(
            self.turn_message,
            font_size=70,
            font_color=(255, 255, 255)
        )
        
        self.menu.add.vertical_margin(30)
        
        # Add game stats as simple text
        stats = self.game.statistics
        stats_text = f"Turns: {stats['turns_played']}  |  Tiles Drawn: {stats['tiles_drawn']}  |  Sets Formed: {stats['valid_sets_formed']}"
        
        self.menu.add.label(
            stats_text,
            font_size=30,
            font_color=(180, 220, 180)
        )
        
        self.menu.add.vertical_margin(10)
        
    def create_tip(self):
        """Add a helpful game tip."""
        tips = [
            "Group tiles of the same value but different colors for a set.",
            "Build runs with consecutive numbers of the same color.",
            "The first move must total at least 30 points.",
            "Plan ahead! Think about your next move while others play.",
            "You can rearrange tiles already on the board during your turn.",
            "Draw a tile if you can't make a valid move."
        ]
        tip_text = random.choice(tips)
        
        self.menu.add.vertical_margin(50)
        
        self.menu.add.label(
            "TIP",
            font_size=28,
            font_color=(255, 255, 180)
        )
        
        self.menu.add.label(
            tip_text,
            font_size=26,
            font_color=(200, 200, 200),
            max_char=60
        )
    
    def create_continue_button(self):
        """Add a simple continue button."""
        self.menu.add.vertical_margin(60)
        
        button = self.menu.add.button(
            "START TURN",
            self.continue_turn,
            font_size=50,
            background_color=(30, 120, 30)
        )
        
        button.set_padding((20, 15))
        
    def continue_turn(self):
        """Sets up the player's rack and switches to the main game screen."""
        self.game.populate_rack()
        self.game.save_positions()
        self.game.change_screen(self.game.game_screen)

    def handle_events(self, events):
        self.menu.update(events)

    def update(self):
        pass

    def draw(self, surface):
        # Fill with a solid background to avoid seeing the game screen behind
        surface.fill((0, 60, 20))
        
        # Add a simple border
        border_width = 8
        pygame.draw.rect(
            surface,
            (0, 40, 0),
            pygame.Rect(0, 0, surface.get_width(), surface.get_height()),
            border_width
        )
        
        # Draw the menu
        self.menu.draw(surface)