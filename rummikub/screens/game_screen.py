import pygame
from rummikub.tile import Tile
from rummikub.board import Board
from rummikub.player import Player
from rummikub.theme_manager import ThemeManager
from rummikub.message_system import MessageSystem

class GameScreen:
    """
    Main game screen that handles rendering and interaction with the game board.
    
    This screen shows the game board, player rack, and game controls.
    It handles tile interaction, move validation, and visual feedback.
    """

    def __init__(self, game):
        """
        Initialize the game screen.
        
        Args:
            game: The main game instance
        """
        self.game = game
        self.screen = pygame.display.set_mode((3400, 2500))
        self.board = Board(game)
        self.dragging = None
        self.dragged_tile = None
        self.dragged_from = None
        
        # Initialize theme and feedback systems
        ThemeManager.initialize()
        self.message_system = MessageSystem()

        # Load images
        self.draw_button_img = pygame.image.load("./rummikub/assets/buttons/draw_button.png")
        self.end_button_img = pygame.image.load("./rummikub/assets/buttons/end_turn_button.png")
        # Create a new reset button image or use a placeholder for now
        try:
            self.reset_button_img = pygame.image.load("./rummikub/assets/buttons/reset_button.png")
        except:
            # If the reset button image doesn't exist, create a similar sized surface
            self.reset_button_img = pygame.Surface(self.end_button_img.get_size())
            self.reset_button_img.fill((50, 100, 200))  # Blue background
        
        self.player_rack_img = pygame.image.load("./rummikub/assets/rack.png")
        self.player_rack_rect = self.player_rack_img.get_rect(midbottom=(1700, 2500))
        
        # Calculate button positions based on player rack position
        right_side_x = 3300  # Position from right edge of screen
        
        # Calculate the vertical center of the player rack
        rack_center_y = self.player_rack_rect.centery
        
        # Button spacing - adjust as needed
        button_spacing = 150  # Vertical spacing between buttons
        
        # Position buttons vertically centered relative to the rack
        # with the middle button (End Turn) aligned with rack center
        self.draw_button_rect = self.draw_button_img.get_rect(
            center=(right_side_x, rack_center_y - button_spacing)
        )
        
        self.end_button_rect = self.end_button_img.get_rect(
            center=(right_side_x, rack_center_y)
        )
        
        self.reset_button_rect = self.reset_button_img.get_rect(
            center=(right_side_x, rack_center_y + button_spacing)
        )
        
        # Create semi-transparent surfaces for board area
        self.board_area = pygame.Surface((3400, 1760), pygame.SRCALPHA)
        self.board_area.fill((*ThemeManager.get_color('board_area')[:3], 128))
        
        # Track hover state for buttons
        self.draw_button_hover = False
        self.end_button_hover = False
        self.reset_button_hover = False
        
        # Try to initialize sound system
        try:
            pygame.mixer.init()
            self.sound_enabled = True
            self.load_sounds()
        except:
            self.sound_enabled = False
            print("Sound system initialization failed. Sounds disabled.")

    def load_sounds(self):
        """Load game sound effects."""
        # These paths assume you'll create/acquire these sound files
        self.sounds = {
            'tile_place': pygame.mixer.Sound('./rummikub/assets/sounds/tile_place.wav'),
            'invalid_move': pygame.mixer.Sound('./rummikub/assets/sounds/invalid_move.wav'),
            'draw_tile': pygame.mixer.Sound('./rummikub/assets/sounds/draw_tile.wav'),
            'valid_set': pygame.mixer.Sound('./rummikub/assets/sounds/valid_set.wav'),
            'win': pygame.mixer.Sound('./rummikub/assets/sounds/win.wav')
        }

    def play_sound(self, sound_name):
        """
        Play a sound effect if available.
        
        Args:
            sound_name (str): Name of the sound to play
        """
        if self.sound_enabled and sound_name in self.sounds:
            self.sounds[sound_name].play()

    def handle_events(self, events):
        # Update hover states for buttons
        mouse_pos = pygame.mouse.get_pos()
        self.draw_button_hover = self.draw_button_rect.collidepoint(mouse_pos)
        self.end_button_hover = self.end_button_rect.collidepoint(mouse_pos)
        self.reset_button_hover = self.reset_button_rect.collidepoint(mouse_pos)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Handle button clicks with visual/audio feedback
                if self.draw_button_rect.collidepoint(mouse_pos):
                    if self.board.added_tiles:
                        self.message_system.add_message(
                            "Cannot draw while tiles are on the board!",
                            color_name='invalid'
                        )
                        self.play_sound('invalid_move')
                    else:
                        self.game.players[self.game.current_turn].draw_tile()
                        self.message_system.add_message(
                            f"{self.game.players[self.game.current_turn].name} drew a tile.",
                            color_name='highlight'
                        )
                        self.game.statistics['tiles_drawn'] += 1
                        self.play_sound('draw_tile')
                        self.game.next_turn()
                
                elif self.end_button_rect.collidepoint(mouse_pos):
                    # Modified behavior: Check validity but don't reset on invalid
                    if self.game.validate_turn():
                        self.message_system.add_message(
                            "Valid move! Turn completed.",
                            color_name='valid'
                        )
                        self.play_sound('valid_set')
                        
                        if self.game.check_for_win():
                            winner = self.game.players[self.game.current_turn].name
                            self.message_system.add_message(
                                f"{winner} wins the game!",
                                color_name='highlight',
                                duration=5.0,
                                font_name='title'
                            )
                            self.play_sound('win')
                            # Could add a win screen transition here
                        else:
                            self.game.next_turn()
                    else:
                        # Just show message but don't reset tiles
                        self.message_system.add_message(
                            "Invalid move! Use Reset button to return tiles to previous positions.",
                            color_name='invalid'
                        )
                        self.game.statistics['invalid_moves'] += 1
                        self.play_sound('invalid_move')
                
                elif self.reset_button_rect.collidepoint(mouse_pos):
                    # New functionality: Reset tiles to previous positions
                    self.board.reset_board()
                    self.message_system.add_message(
                        "Tiles reset to start of turn.",
                        color_name='highlight'
                    )
                    self.play_sound('tile_place')
                
                # Continue with original tile dragging code
                # Check player rack first
                for tile in self.game.players[self.game.current_turn].tiles.values():
                    if tile.rect.collidepoint(mouse_pos):
                        tile.start_drag(mouse_pos)
                        self.dragged_tile = tile
                        self.dragged_from = 'rack'
                        break
                
                # If not in rack, check board tiles
                if self.dragged_tile is None:
                    for tile in self.board.tiles.values():
                        if tile.rect.collidepoint(mouse_pos):
                            tile.start_drag(mouse_pos)
                            self.dragged_tile = tile
                            self.dragged_from = 'board'
                            break

            elif event.type == pygame.MOUSEMOTION and self.dragged_tile:
                self.dragged_tile.update_drag(pygame.mouse.get_pos())
                
                # Provide visual feedback during dragging
                if self.is_on_board(self.dragged_tile.rect):
                    valid_drop = self.is_valid_drop(self.dragged_tile, self.board.tiles)
                    self.dragged_tile.set_highlight(True, 'valid' if valid_drop else 'invalid')
                else:
                    self.dragged_tile.set_highlight(False)

            elif event.type == pygame.MOUSEBUTTONUP and self.dragged_tile:
                self.dragged_tile.stop_drag()
                self.dragged_tile.set_highlight(False)  # Clear highlight
                
                # Process the drop with audio feedback
                if self.dragged_from == 'rack':
                    if self.is_on_board(self.dragged_tile.rect) and self.is_valid_drop(self.dragged_tile, self.board.tiles):
                        # Valid drop from rack to board
                        self.game.players[self.game.current_turn].remove_tile(self.dragged_tile.id)
                        self.board.add_tile(self.dragged_tile)
                        self.board.update_sets()
                        self.board.snap_tile(self.dragged_tile)
                        self.play_sound('tile_place')
                    else:
                        # Invalid drop: revert to pre-drag position
                        self.dragged_tile.revert_to_pre_drag()
                        self.play_sound('invalid_move')
                        
                elif self.dragged_from == 'board':
                    if self.is_on_board(self.dragged_tile.rect):
                        # Dropped within board, check for collisions
                        if not self.is_valid_drop(self.dragged_tile, self.board.tiles):
                            # Collision detected: revert movement
                            self.dragged_tile.revert_to_pre_drag()
                            self.play_sound('invalid_move')
                        else:
                            # Valid move within board
                            self.board.update_sets()
                            self.board.snap_tile(self.dragged_tile)
                            self.play_sound('tile_place')
                    else:
                        # Dropped outside board
                        if self.dragged_tile.id in self.board.added_tiles:
                            # Allow removal back to rack
                            removed_tile = self.board.remove_tile(self.dragged_tile.id)
                            if removed_tile:
                                self.game.players[self.game.current_turn].add_tile(removed_tile)
                                self.play_sound('tile_place')
                        else:
                            # Pre-existing board tile: revert to its turn start
                            self.dragged_tile.revert_to_turn_start()
                            self.play_sound('invalid_move')
                
                self.dragged_tile = None
                self.dragged_from = None

    def update(self):
        """Update game screen components."""
        self.message_system.update()

    def render(self):
        """Render the game screen with all UI components."""
        # Clear screen with theme background
        self.screen.fill(ThemeManager.get_color('background'))
        
        # Draw board area with semi-transparent overlay
        self.screen.blit(self.board_area, (0, 0))
        
        # Draw current player indicator
        current_player = self.game.players[self.game.current_turn]
        player_text = ThemeManager.render_text(
            f"Current Player: {current_player.name}",
            font_name='heading',
            color_name='highlight'
        )
        self.screen.blit(player_text, (20, 20))
        
        # Draw deck info
        deck_text = ThemeManager.render_text(
            f"Tiles in deck: {len(self.game.deck)}",
            font_name='normal',
            color_name='text'
        )
        self.screen.blit(deck_text, (20, 80))
        
        # Draw player rack and UI elements
        self.screen.blit(self.player_rack_img, self.player_rack_rect)
        
        # Draw themed buttons in their new positions
        ThemeManager.draw_button(
            self.screen, 
            self.draw_button_rect,
            "Draw Tile",
            color_name='button_success',
            hover=self.draw_button_hover
        )
        
        ThemeManager.draw_button(
            self.screen, 
            self.end_button_rect,
            "End Turn",
            color_name='button_danger',
            hover=self.end_button_hover
        )
        
        # Draw the new Reset Tiles button
        ThemeManager.draw_button(
            self.screen, 
            self.reset_button_rect,
            "Reset Tiles",
            color_name='button_info',  # Assuming 'button_info' exists in your theme
            hover=self.reset_button_hover
        )
        
        # Draw player tiles and board
        self.draw_player_tiles()
        self.board.draw(self.screen)
        
        # Draw messages last (on top)
        self.message_system.draw(self.screen)
        
        pygame.display.update()


    def draw_player_tiles(self) -> None:
        self.game.players[self.game.current_turn].draw(self.screen)

    def is_on_board(self, tile) -> None:
        return tile.x < 3400 and tile.y < 1760

    def is_valid_drop(self, tile, container):
        # 'container' could be a dictionary of tiles from the board or rack.
        for other in container.values():
            if other.id != tile.id and tile.rect.colliderect(other.rect):
                return False
        return True
    
    def draw(self):
        pass