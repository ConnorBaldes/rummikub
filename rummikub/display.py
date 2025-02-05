from termcolor import colored

def display_tile(tile):
    """
    Return a string representation of a single tile with its color applied.
    """
    if tile.is_joker:
        return colored("[J]", "white", attrs=["bold", "blink"])
    
    color_map = {
        "red": "red",
        "blue": "blue",
        "orange": "yellow",
        "black": "grey",
    }
    color = color_map.get(tile.color, "white")
    return colored(f"[{tile.number}]", color, attrs=["bold"])

def display_tiles(tiles, numbered=False):
    """
    Return a formatted string representation of a list of tiles with colors applied.
    If `numbered` is True, add selection numbers for player convenience.
    """
    if numbered:
        return ", ".join(f"{i+1}: {display_tile(tile)}" for i, tile in enumerate(tiles))
    return ", ".join(display_tile(tile) for tile in tiles)

def display_board(board):
    """
    Display the board with clearer sectioning and improved visualization.
    """
    print("\n" + colored("=" * 40, "cyan", attrs=["bold"]))
    print(colored(" 📌 CURRENT BOARD ", "cyan", attrs=["bold"]))
    print(colored("=" * 40, "cyan", attrs=["bold"]))

    if not board.sets:
        print(colored("The board is empty. Start playing!", "yellow"))
        return

    for i, tile_set in enumerate(board.sets):
        sorted_set = sorted(tile_set, key=lambda tile: (tile.number if tile.number else float('inf')))
        print(f"{i+1}. {display_tiles(sorted_set)}")

    print(colored("=" * 40, "cyan", attrs=["bold"]) + "\n")

def display_player_turn(player):
    """
    Display the current player's turn with a clear indicator.
    """
    print("\n" + colored("=" * 40, "green", attrs=["bold"]))
    print(colored(f" 🎲 {player.name.upper()}'S TURN 🎲", "green", attrs=["bold", "underline"]))
    print(colored("=" * 40, "green", attrs=["bold"]))

def display_hand(player):
    """
    Display the player's hand with numbered tiles for easy selection.
    """
    print(colored(f"Your Hand:", "magenta", attrs=["bold"]))
    print(display_tiles(player.hand, numbered=True))
