class Player:

    def __init__(self, player_num):
        self.player_num = (player_num)
        self.tile_rack = []
        self.initial_meld = False

    def add_tile_to_rack(self, tile):
        # Add a tile to the player's hand
        self.tile_rack.append(tile)