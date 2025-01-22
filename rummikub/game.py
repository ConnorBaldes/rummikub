from rummikub.deck import Deck
from rummikub.board import Board
from rummikub.player import Player

class Game:
    def __init__(self, players):
        self.deck = Deck()
        self.board = Board()
        self.players = [Player(name) for name in players]
        self.current_player_index = 0

    def start(self):
        # Deal tiles to players
        for player in self.players:
            for _ in range(14):
                player.draw(self.deck)

    def next_turn(self):
        # Handle player turn logic
        pass
