import os
import pygame
import pygame_menu
from pygame_menu import themes, BaseImage
from rummikub.player import Player

class SetupMenu:
    """Initial game setup menu with structured game information and horizontal visual examples."""

    def __init__(self, game):
        self.game = game

        # Define a custom theme with the desired background color
        custom_theme = themes.THEME_DARK.copy()
        custom_theme.background_color = (0, 128, 0)  # Green background
        custom_theme.title_font_size = 60
        custom_theme.widget_font_size = 40
        custom_theme.widget_font_color = (255, 255, 255)  # White text

        self.menu = pygame_menu.Menu(
            title="Welcome to Rummikub",
            width=game.screen.get_width(),
            height=game.screen.get_height(),
            theme=custom_theme
        )

        # Game Objective
        self.menu.add.label("Game Objective", font_size=50, font_color=(255, 255, 0))
        self.menu.add.label(
            "Be the first to play all your tiles by forming valid sets.",
            max_char=140,
            font_size=36
        )
        self.menu.add.vertical_margin(20)

        # Rules Summary
        self.menu.add.label("Rules Summary", font_size=50, font_color=(255, 255, 0))
        rules = [
            "Sets: Groups (same number, different colors) or Runs (consecutive numbers, same color).",
            "Initial Meld: Must total at least 30 points using tiles from your rack.",
            "Tile Manipulation: Rearrange the board, ensuring all sets remain valid.",
            "If you can't play, draw a tile and pass your turn."
        ]
        for rule in rules:
            self.menu.add.label(rule, max_char=140, font_size=32)
        self.menu.add.vertical_margin(20)

        # Visual Examples
        self.menu.add.label("Examples of Valid Sets and Runs", font_size=50, font_color=(255, 255, 0))
        self.add_example_images()
        self.menu.add.vertical_margin(20)

        # Player Name Input
        self.menu.add.label("Enter Player Names (2-4 Players)", font_size=50, font_color=(0, 255, 255))
        self.name_input = self.menu.add.text_input(
            title="Names: ",
            default="Connor, Elsa",
            maxchar=100,
            font_size=42,
            textinput_id="name_input",
            # cursor_color=(255, 255, 255),
            background_color=(50, 50, 50),
            border_width=2,
            border_color=(255, 255, 255)
        )
        self.menu.add.vertical_margin(20)

        # Buttons
        self.menu.add.button("Submit Names", self.submit_names, font_size=50, background_color=(50, 200, 50))
        self.menu.add.button("Quit", pygame_menu.events.EXIT, font_size=50, background_color=(200, 50, 50))

    def add_example_images(self):
        """Add visual examples of valid sets and runs using tile images."""
        # Example 1: Group (same number, different colors)
        group_tiles = ["tile_5_red.png", "tile_5_blue.png", "tile_5_black.png"]
        self.add_tile_row(group_tiles, "Example of a Group: Same number, different colors")

        # Example 2: Run (consecutive numbers, same color)
        run_tiles = ["tile_7_orange.png", "tile_8_orange.png", "tile_9_orange.png"]
        self.add_tile_row(run_tiles, "Example of a Run: Consecutive numbers, same color")

    def add_tile_row(self, tile_filenames, description):
        """Add a horizontal row of tile images with a description to the menu."""
        tile_images = []
        tile_width, tile_height = 140, 240  # Tile size for display
        gap = 10  # Space between tiles

        for filename in tile_filenames:
            tile_path = os.path.join("./rummikub/assets/tiles/", filename)
            if os.path.exists(tile_path):
                tile_images.append(pygame.image.load(tile_path))
            else:
                print(f"Warning: Missing image {filename}, using placeholder.")
                placeholder_path = os.path.join("./rummikub/assets/tiles/placeholder.png")
                if os.path.exists(placeholder_path):
                    tile_images.append(pygame.image.load(placeholder_path))

        if tile_images:
            # Create a surface to hold the row of tiles
            tile_row_width = sum(img.get_width() for img in tile_images) + (len(tile_images) - 1) * gap
            tile_row_height = max(img.get_height() for img in tile_images)
            tile_row_surface = pygame.Surface((tile_row_width, tile_row_height), pygame.SRCALPHA)

            # Blit tiles onto the row surface
            x_offset = 0
            for image in tile_images:
                scaled_image = pygame.transform.scale(image, (tile_width, tile_height))
                tile_row_surface.blit(scaled_image, (x_offset, 0))
                x_offset += tile_width + gap

            # If BaseImage requires a file path, save the surface as an image file first
            tile_row_surface_path = "./rummikub/assets/tiles/tile_row.png"
            pygame.image.save(tile_row_surface, tile_row_surface_path)

            # Convert the surface into a BaseImage and add it to the menu
            tile_row_image = BaseImage(image_path=tile_row_surface_path)
            self.menu.add.image(tile_row_image)

        # Add description label
        self.menu.add.label(description, font_size=32, font_color=(255, 255, 255))
        self.menu.add.vertical_margin(10)


    def submit_names(self):
        """Validate player names and transition to the first turn."""
        names = [name.strip() for name in self.name_input.get_value().split(",") if name.strip()]
        if 2 <= len(names) <= 4:
            self.game.players = [Player(self.game, name) for name in names]
            self.game.current_turn = 0  # Start with the first player
            self.game.populate_rack()
            self.game.save_positions()

            # Transition to the first player's turn menu
            turn_message = f"{self.game.players[self.game.current_turn].name}, press Continue to start your turn."
            self.game.change_screen(TurnMenu(self.game, turn_message))
        else:
            self.menu.add.label("Invalid input! Please enter 2 to 4 names.", font_color=(255, 0, 0), font_size=40)

    def handle_events(self, events):
        self.menu.update(events)

    def update(self):
        pass

    def draw(self, surface):
        self.menu.draw(surface)


class TurnMenu:
    """Displays the current player's turn and prompts them to continue."""

    def __init__(self, game, turn_message):
        self.game = game
        self.turn_message = turn_message

        # Define a custom theme consistent with SetupMenu
        custom_theme = themes.THEME_DARK.copy()
        custom_theme.background_color = (0, 128, 0)  # Green background
        custom_theme.title_font_size = 60
        custom_theme.widget_font_size = 40
        custom_theme.widget_font_color = (255, 255, 255)  # White text

        self.menu = pygame_menu.Menu(
            title="Player Turn",
            width=game.screen.get_width(),
            height=game.screen.get_height(),
            theme=custom_theme
        )

        self.add_turn_display()
        self.add_continue_button()

    def add_turn_display(self):
        """Add turn message display."""
        self.menu.add.label(self.turn_message, font_size=50, font_color=(255, 255, 0))
        self.menu.add.vertical_margin(30)

    def add_continue_button(self):
        """Add button to continue the turn."""
        self.menu.add.button("Continue", self.continue_turn, font_size=50, background_color=(50, 200, 50))
        self.menu.add.vertical_margin(20)

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
        self.menu.draw(surface)

