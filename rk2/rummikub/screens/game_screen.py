import pygame
from rummikub.tile import Tile
from rummikub.board import Board
from rummikub.player import Player


class GameScreen:
    def __init__(self, game):

        self.game = game
        self.board = Board()
        self.draw_button = None
        self.end_button = None
        self.dragging_tile = None


    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass  # Handle tile selection logic
            elif event.type == pygame.MOUSEMOTION:
                pass  # Handle tile dragging logic
            elif event.type == pygame.MOUSEBUTTONUP:
                pass  # Handle tile placement logic

    def update(self):
        self.board.update_sets()
    
    def render(self, screen):
        screen.fill((255, 255, 255))  # Clear screen
        self.board.draw(screen)