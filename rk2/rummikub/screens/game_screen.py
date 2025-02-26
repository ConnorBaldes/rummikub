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
        self.dragged_tile = None
        self.dragged_from = None

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
                mouse_pos = pygame.mouse.get_pos()
                # Check player rack first.
                for tile in self.game.players[self.game.current_turn].tiles.values():
                    if tile.rect.collidepoint(mouse_pos):
                        tile.start_drag(mouse_pos)
                        self.dragged_tile = tile
                        self.dragged_from = 'rack'
                        break
                # If not in rack, check board tiles (all are draggable on board).
                if self.dragged_tile is None:
                    for tile in self.board.tiles.values():
                        if tile.rect.collidepoint(mouse_pos):
                            tile.start_drag(mouse_pos)
                            self.dragged_tile = tile
                            self.dragged_from = 'board'
                            break


                if self.draw_button_rect.collidepoint(event.pos):
                    self.game.players[self.game.current_turn].draw_tile()
                    self.game.next_turn()
                elif self.end_button_rect.collidepoint(event.pos):
                    if self.board.validate_sets():
                        self.game.next_turn()
                    else:
                        # TO DO: Reset tiles
                        pass

            elif event.type == pygame.MOUSEMOTION and self.dragged_tile:
                self.dragged_tile.update_drag(pygame.mouse.get_pos())

            elif event.type == pygame.MOUSEBUTTONUP and self.dragged_tile:
                self.dragged_tile.stop_drag()
                # Decide where the tile was dropped:
                if self.dragged_from == 'rack':
                    if self.is_on_board(self.dragged_tile.rect) and self.is_valid_drop(self.dragged_tile, self.board.tiles):
                        # Valid drop from rack to board.
                        self.game.players[self.game.current_turn].remove_tile(self.dragged_tile.id)
                        self.board.add_tile(self.dragged_tile)
                        self.board.update_sets()
                        self.board.snap_tile(self.dragged_tile)
                        
                    else:
                        # Invalid drop: revert to pre-drag position.
                        self.dragged_tile.revert_to_pre_drag()
                elif self.dragged_from == 'board':
                    if self.is_on_board(self.dragged_tile.rect):
                        # Dropped within board, but check for collisions.
                        if not self.is_valid_drop(self.dragged_tile, self.board.tiles):
                            # Collision detected: revert movement.
                            self.dragged_tile.revert_to_pre_drag()
                        # Else: leave tile at new board position.
                        self.board.update_sets()
                        self.board.snap_tile(self.dragged_tile)
                        
                    else:
                        # Dropped outside board.
                        if self.dragged_tile.id in self.board.added_tiles:
                            # Allow removal back to rack.
                            removed_tile = self.board.remove_tile(self.dragged_tile.id)
                            if removed_tile:
                                self.game.players[self.game.current_turn].add_tile(removed_tile)
                        else:
                            # Pre-existing board tile: revert to its turn start.
                            self.dragged_tile.revert_to_turn_start()
                self.dragged_tile = None
                self.dragged_from = None

    def update(self):
        pass
    
    def render(self):
        self.screen.fill((0, 128, 0))  # Clear screen
 
        # Draw player rack and board buttons
        self.screen.blit(self.draw_button_img, self.draw_button_rect.topleft)
        self.screen.blit(self.end_button_img, self.end_button_rect.topleft)
        self.screen.blit(self.player_rack_img, self.player_rack_rect)
        self.draw_player_tiles()
        # Draw board tiles
        self.board.draw(self.screen)
        
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


    # Function to check if a dragged tile collides with any other tile
    def check_overlap(self, dragged_tile):
        for other_tile in self.board.get_tile_positions():
            if other_tile.id != dragged_tile.id and dragged_tile.rect.colliderect(other_tile.rect):
                return True  # Collision detected
        return False