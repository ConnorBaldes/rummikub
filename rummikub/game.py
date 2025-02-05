import copy
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
        self.saved_state = None  # Stores the saved state for rollback

    def start(self):
        """Initialize the game, determine turn order, and deal tiles."""
        self._determine_turn_order()
        self._deal_tiles()

    def _determine_turn_order(self):
        """Decide turn order by drawing a tile."""
        turn_order = []
        for player in self.players:
            tile = player.draw_tile(self.deck)
            print(f"{player.name} picked {display_tile(tile)}")
            turn_order.append((player, tile))

        turn_order.sort(key=lambda x: (x[1].is_joker, x[1].number), reverse=True)
        self.players = [entry[0] for entry in turn_order]

        print("Turn order decided:")
        for i, player in enumerate(self.players, 1):
            print(f"{i}. {player.name}")

    def _deal_tiles(self):
        """Deal 13 tiles to each player."""
        for player in self.players:
            for _ in range(13):
                player.draw_tile(self.deck)

    def save_state(self):
        """Save a deep copy of the game state at the start of a turn."""
        self.saved_state = {
            "player_hand": copy.deepcopy(self.players[self.current_player_index].hand),
            "player_initial_meld": self.players[self.current_player_index].initial_meld,
            "board_sets": copy.deepcopy(self.board.sets),
            "staging": copy.deepcopy(self.board.staging),
            "deck_tiles": copy.deepcopy(self.deck.tiles),
        }

    def restore_state(self):
        """Restore the game state from the last saved snapshot."""
        if self.saved_state:
            self.players[self.current_player_index].hand = self.saved_state["player_hand"]
            self.players[self.current_player_index].initial_meld = self.saved_state["player_initial_meld"]
            self.board.sets = self.saved_state["board_sets"]
            self.board.staging = self.saved_state["staging"]
            self.deck.tiles = self.saved_state["deck_tiles"]
            print("❌ Invalid move detected. Board reset to previous state.")

    def next_turn(self):
        """Handle a player's turn, allowing full board manipulation."""
        current_player = self.players[self.current_player_index]
        print(f"\n{current_player.name}'s turn")
        
        # Save the initial game state
        self.save_state()

        while True:
            print("\n🔹 Current Board:")
            display_board(self.board)

            print(f"\n🔸 Your Hand: {display_tiles(current_player.hand, numbered=True)}")

            # Player manipulates the board freely
            self._handle_board_manipulation(current_player)

            # Validate the board and the move
            if self._validate_turn(current_player):
                break  # Move is valid, proceed to next turn
            else:
                self.restore_state()  # Restore game state and retry

        # Move to the next player's turn
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def _handle_board_manipulation(self, player):
        """Let the player freely manipulate tiles before confirming their move."""
        print("💡 You can freely move tiles between your hand, board, and staging area.")
        print("🔄 Type 'done' when finished.")
        
        while True:
            action = input("Enter a move (play/move/done): ").strip().lower()

            if action == "done":
                break
            elif action == "play":
                self._handle_play(player)
            elif action == "move":
                self._handle_move()
            else:
                print("Invalid input. Type 'play', 'move', or 'done'.")

    def _handle_play(self, player):
        """Allow the player to play tiles from their hand."""
        try:
            indices = input("Enter tile indices to play (comma-separated): ")
            tile_indices = list(map(int, indices.split(',')))
            tiles_to_play = [player.hand[i] for i in tile_indices]

            set_choice = input("Play tiles in a new set or existing set? (new/existing): ").strip().lower()
            if set_choice == "new":
                self.board.add_set(tiles_to_play)
                player.play_tiles(tiles_to_play)
            elif set_choice == "existing":
                set_index = int(input("Enter set index to add tiles to: ")) - 1
                self.board.add_to_set(set_index, tiles_to_play)
                player.play_tiles(tiles_to_play)
            else:
                print("Invalid choice. Try again.")

        except Exception as e:
            print(f"❌ Error: {e}")

    def _handle_move(self):
        """Allow moving tiles between board sets and staging area."""
        try:
            print("\n🔄 Moving tiles between sets.")
            src_set = int(input("Enter source set index (or 0 for staging area): ")) - 1
            tile_index = int(input("Enter the tile index within the set: "))
            dest_set = int(input("Enter destination set index (or 0 for staging area): ")) - 1

            if src_set == -1:
                tile = self.board.staging.pop(tile_index)
            else:
                tile = self.board.sets[src_set].pop(tile_index)

            if dest_set == -1:
                self.board.staging.append(tile)
            else:
                self.board.sets[dest_set].append(tile)

            print("✅ Move successful.")

        except Exception as e:
            print(f"❌ Error: {e}")

    def _validate_turn(self, player):
        """Validate if the board is in a valid state after a player's turn."""
        if not all(self.board.is_valid_set(s) for s in self.board.sets):
            print("❌ Invalid board state. Some sets are incorrect.")
            return False

        if self.board.staging:
            print("❌ The staging area must be empty before ending your turn.")
            return False

        if not any(tile not in player.hand for s in self.board.sets for tile in s):
            print("❌ You must play at least one tile from your hand.")
            return False

        print("✅ Move accepted. Next player's turn.")
        return True
