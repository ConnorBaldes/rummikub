from rummikub.deck import Deck
from rummikub.board import Board
from rummikub.player import Player
from rummikub.display import display_board, display_tiles, display_tile

class Game:
    def __init__(self, players: list[Player]):
        self.deck = Deck()
        self.board = Board()
        self.players = [Player(name) for name in players]
        self.current_player_index = 0


    def start(self):
        """
        Initialize the game by determining turn order and dealing tiles to players.
        Each player picks a single tile to decide the turn order.
        """
        self._determine_turn_order()
        self._deal_tiles()

    def _determine_turn_order(self):
        """
        Each player draws a single tile to decide the turn order.
        """
        turn_order = []
        for player in self.players:
            tile = player.draw_tile(self.deck)
            print(f"{player.name} picked {display_tile(tile)}")
            turn_order.append((player, tile))

        # Sort players by tile value, with Joker beating all numbers
        turn_order.sort(key=lambda x: (x[1].is_joker, x[1].number), reverse=True)

        # Reorder players based on the sorted turn order
        self.players = [entry[0] for entry in turn_order]
        print("Turn order decided:")
        for i, player in enumerate(self.players, 1):
            print(f"{i}. {player.name}")

    def _deal_tiles(self):
        """
        Deal the remaining tiles to players.
        """
        for player in self.players:
            for _ in range(13):  # 14 total tiles minus the one already picked
                player.draw_tile(self.deck)

    def next_turn(self):
        """
        Handle the flow of a player's turn.
        """
        current_player = self.players[self.current_player_index]
        print(f"\n{current_player.name}'s turn")
        print(f"Your hand: {display_tiles(current_player.hand)}")

        while True:
            # Display the current board state
            print("Current board:")
            display_board(self.board)  # Use display module

            # Get player input for their action
            action = input("Choose an action: (play, draw): ").strip().lower()
            move_made = False
            while action == "play":
                if self._handle_play(current_player):
                    move_made = True
                    print("Current board:")
                    display_board(self.board)
                    print(f"Your hand: {display_tiles(current_player.hand)}")
                    action = input("Would you like to play more tiles or pass: (play, pass): ").strip().lower()
                elif move_made:
                    action = input("Would you like to try a different move or pass: (play, pass): ").strip().lower()
                else:
                    action = input("Would you like to try a different move or draw: (play, draw): ").strip().lower()
                    
            if action == "draw":
                self._handle_draw(current_player)
                break
            elif action == "pass":
                print(f"{current_player.name} passes")
                break
            else:
                print("Invalid action.")

        # Move to the next player's turn
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def _handle_play(self, player) -> bool:
        """
        Handle a player's attempt to play tiles onto the board.
        """
        try:
            # Ask the player to input the indices of tiles they want to play
            indices = input("Enter the indices of the tiles to play (comma-separated): ")
            tile_indices = list(map(int, indices.split(',')))
            tiles_to_play = [player.hand[i] for i in tile_indices]

            if player.initial_meld:
                # Ask for target position on the board or create a new set
                target = input("Play tiles in a new set or existing set? (new/existing): ").strip().lower()
                if target == "new":
                    self.board.add_set(tiles_to_play)
                    player.play_tiles(tiles_to_play)
                    print("Tiles successfully played as a new set.")
                    return True  # Return True to tell next_turn() play was valid
                elif target == "existing":
                    set_index = int(input("Enter the index of the set to add tiles to: "))
                    self.board.add_to_set(set_index, tiles_to_play)
                    player.play_tiles(tiles_to_play)
                    print("Tiles successfully added to the existing set.")
                    return True
                else:
                    print("Invalid option. Tiles not played.")
                    return False  # Return False to tell next_turn() play was not valid
            
            else:
                    if self._initial_meld_valid(player, tiles_to_play):
                        self.board.add_set(tiles_to_play)
                        player.play_tiles(tiles_to_play)
                        return True
                    else:
                        return False

        except Exception as e:
            print(f"Error during play: {e}")
            return False

    def _handle_draw(self, player):
        """
        Handle a player drawing a tile from the deck.
        """
        if not self.deck.is_empty():
            tile = self.deck.draw_tile()
            player.hand.append(tile)
            print(f"{player.name} drew a tile: {display_tile(tile)}")
        else:
            print("The deck is empty. No tiles to draw.")

    def _initial_meld_valid(self, player, tiles_to_play) -> bool:
        """
        Check if the tiles selected by the player for the initial meld 
        form a valid set and add up to at least 30 points, considering jokers.
        """
        try:

            # Check if the selected tiles form a valid set on the board
            if not self.board.is_valid_set(tiles_to_play):
                print("Selected tiles do not form a valid set.")
                return False

            total_points = 0
            for tile in tiles_to_play:
                if tile.is_joker:
                    # Handle joker by assuming it represents the largest value in the set
                    max_value = self._get_max_value_in_set(tiles_to_play)
                    total_points += max_value
                else:
                    total_points += tile.number

            # Check if the sum of points is greater than or equal to 30
            if total_points >= 30:
                print(f"Initial meld is valid. Total points: {total_points}")
                player.initial_meld = True
                return True
            else:
                print(f"Initial meld is invalid. Total points: {total_points}. Must be at least 30.")
                return False

        except IndexError:
            print("Error: Invalid tile indices.")
            return False

    def _get_max_value_in_set(self, tiles_to_play):
        """
        Given a set of tiles, find the highest number that the joker can represent.
        """
        # Sort the tiles by their number (ignoring jokers)
        non_joker_tiles = [tile for tile in tiles_to_play if not tile.is_joker]
        if not non_joker_tiles:
            return 0  # If no non-joker tiles, the joker cannot represent anything meaningful

        sorted_tiles = sorted(non_joker_tiles, key=lambda tile: tile.number)
        # The joker should represent the next valid number in the sequence
        return sorted_tiles[-1].number + 1  # Joker represents the next number in the set
