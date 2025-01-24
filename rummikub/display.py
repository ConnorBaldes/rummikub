from termcolor import colored

def display_tile(tile):
    """
    Return a string representation of a single tile with its color applied.
    """
    if tile.is_joker:
        return colored("[J]", "white", attrs=["bold"])
    color_map = {
        "red": "red",
        "blue": "blue",
        "orange": "yellow",
        "black": "grey",
    }
    color = color_map.get(tile.color, "white")
    return colored(f"[{tile.number}]", color)

def display_tiles(tiles):
    """
    Return a string representation of a list of tiles with colors applied.
    """
    return ", ".join(display_tile(tile) for tile in tiles)

def display_board(board):
    """
    Display the sets on the board, each on its own line.
    Sets that are runs are sorted by number.
    """
    for i, tile_set in enumerate(board.sets):
        sorted_set = sorted(tile_set, key=lambda tile: (tile.number if tile.number else float('inf')))
        print(f"Set {i + 1}: {display_tiles(sorted_set)}")
