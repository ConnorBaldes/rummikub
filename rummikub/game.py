from rummikub.deck import Deck
from rummikub.board import Board
from rummikub.player import Player
from rummikub.display import display_board, display_tiles, display_tile

class Game:
    def __init__(self, players):
        self.deck = Deck()
        self.board = Board()
        self.players = [Player(name) for name in players]
        self.current_player_index = 0

    def start(self):
        """
        Initialize the game by dealing tiles to players.
        """
        for player in self.players:
            for _ in range(14):
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
            action = input("Choose an action: (play, draw, pass): ").strip().lower()

            if action == "play":
                self._handle_play(current_player)
            elif action == "draw":
                self._handle_draw(current_player)
                break
            elif action == "pass":
                print(f"{current_player.name} passes their turn.")
                break
            else:
                print("Invalid action. Try again.")

        # Move to the next player's turn
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def _handle_play(self, player):
        """
        Handle a player's attempt to play tiles onto the board.
        """
        try:
            # Ask the player to input the indices of tiles they want to play
            indices = input("Enter the indices of the tiles to play (comma-separated): ")
            tile_indices = list(map(int, indices.split(',')))
            tiles_to_play = [player.hand[i] for i in tile_indices]

            # Ask for target position on the board or create a new set
            target = input("Play tiles in a new set or existing set? (new/existing): ").strip().lower()

            if target == "new":
                self.board.add_set(tiles_to_play)
                player.play_tiles(tiles_to_play)
                print("Tiles successfully played as a new set.")
            elif target == "existing":
                set_index = int(input("Enter the index of the set to add tiles to: "))
                self.board.add_to_set(set_index, tiles_to_play)
                player.play_tiles(tiles_to_play)
                print("Tiles successfully added to the existing set.")
            else:
                print("Invalid option. Tiles not played.")
        except Exception as e:
            print(f"Error during play: {e}")

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