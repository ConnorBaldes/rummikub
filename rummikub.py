from player import Player
from table import Table
      
class Rummikub:
    def __init__(self, num_players):
        self.players = [Player(player_num) for player_num in range(num_players)]
        self.game_table = Table()


