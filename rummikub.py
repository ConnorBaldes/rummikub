import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--players",
                    choices = [2,3,4],
                    type = int,
                    default=2,
                    help = "Input a number between 2-4 for the number of players.")

class Tile:

    def __init__(self, number, color, value, joker=False):
        self.number = number
        self.color = color
        self.value = value
        self.joker = joker


class Player:


    def __init__(self, player_num):
        self.number = (player_num)
        self.tile_rack = []
    def get_tile_rack(self):
        return self.tile_rack
        
class Table:

    #Table contents
    tile_colors = ['red', 'black', 'blue', 'yellow']
    tile_values = list(range(1,14))
    tile_pool = []
    table_sets = []

    def __init__(self):
        tile_number = 1
        for color in self.tile_colors:
            for value in self.tile_values:
                for _ in range(2):
                    self.tile_pool.append(Tile(number=tile_number, color=color, value=value))
                    tile_number+= 1

        self.tile_pool.append(Tile(number=105, color='joker', value=0))
        self.tile_pool.append(Tile(number=106, color='joker', value=0))

    def get_tile_pool(self):
        return self.tile_pool
    
    def get_tiles_remaining(self):
        return len(self.tile_pool)

    def take_tile(self):
        tile = random.choice(self.tile_pool)
        self.tile_pool.remove(tile)
        return tile

    def get_table_sets(self):
        return self.table_sets
    
    
class Rummikub:

    players = []

    def __init__(self, num_players):    
        for player in range(num_players):
            self.players.append(Player(player))
        self.game_table = Table()

    def player_pick_tile(self, player_num):
        new_tile = self.game_table.take_tile()
        self.players[player_num].tile_rack.append(new_tile)
        
        
    def show_player_rack(self, player_num):
        rack = self.players[player_num].get_tile_rack()
        print(f"Player {player_num} Rack:")
        for tile in rack:
            print(f"{tile.value} {tile.color}")

    def set_initial_racks(self):
        for i in range(14):
            for player in self.players:
                self.player_pick_tile(player.number)

def main():
    args = parser.parse_args()
    game = Rummikub(args.players)

    game.set_initial_racks()

    for player in game.players:
        game.show_player_rack(player.number)
        turn = input("Its your turn")

main()