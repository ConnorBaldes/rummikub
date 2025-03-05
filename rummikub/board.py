import pygame
import math
from rummikub.tile import Tile
from rummikub.utils import Graph
from typing import List, Optional


class Board:
    def __init__(self, game):
        self.game = game
        self.graph: Graph = Graph(106)
        self.tiles = {}  # All board tiles: {tile_id: Tile}
        self.added_tiles = []  # Tile IDs added during current turn

    def add_tile(self, tile: Tile) -> None:
        self.tiles[tile.id] = tile
        self.added_tiles.append(tile.id)

        # Update board graph
        self.graph.add_tile(tile)
    
    def remove_tile(self, tile_id: int):
        # Only reversible if the tile was added on the current turn
        if tile_id in self.added_tiles:
            self.added_tiles.remove(tile_id)
            self.graph.remove_tile_by_id(tile_id)
            return self.tiles.pop(tile_id)
        
        return None
    
    def draw(self, screen) -> None:
        for tile in self.tiles.values():
            tile.draw(screen)
    
    def is_valid_group(self, tiles: list) -> bool:
        """
        Check if tiles form a valid group (same number, different colors).
        
        Args:
            tiles: List of tiles to check
            
        Returns:
            bool: True if tiles form a valid group
        """
        # Must be exactly 3 or 4 tiles
        if len(tiles) not in (3, 4):
            return False
            
        # Separate non-joker tiles
        non_jokers = [tile for tile in tiles if not hasattr(tile, 'is_joker') or not tile.is_joker]
        if not non_jokers:  # There must be at least one non-joker to define the number
            return False
            
        # All non-joker tiles must share the same number
        target_number = non_jokers[0].number
        for tile in non_jokers:
            if tile.number != target_number:
                return False
                
        # Colors of non-joker tiles must be unique
        colors = [tile.color for tile in non_jokers]
        if len(colors) != len(set(colors)):
            return False
            
        return True

    def is_valid_run(self, tiles: list) -> bool:
        """
        Check if tiles form a valid run (same color, sequential numbers).
        
        Args:
            tiles: List of tiles to check
            
        Returns:
            bool: True if tiles form a valid run
        """
        # Must contain at least 3 tiles
        if len(tiles) < 3:
            return False
            
        non_jokers = [tile for tile in tiles if not hasattr(tile, 'is_joker') or not tile.is_joker]
        if not non_jokers:  # Run must have at least one non-joker to set the color
            return False
            
        # All non-joker tiles must be the same color
        run_color = non_jokers[0].color
        for tile in non_jokers:
            if tile.color != run_color:
                return False
                
        # Sort non-joker tiles by their number
        non_jokers.sort(key=lambda tile: tile.number)
        numbers = [tile.number for tile in non_jokers]
        
        # Check that there are no duplicate numbers among non-jokers
        if len(numbers) != len(set(numbers)):
            return False
            
        # Compute the total gaps needed between consecutive numbers
        required_gaps = 0
        for i in range(len(numbers) - 1):
            required_gaps += numbers[i+1] - numbers[i] - 1
            
        available_jokers = len(tiles) - len(non_jokers)
        if required_gaps > available_jokers:
            return False
            
        return True

    def update_sets(self) -> None:
        """Updates sets by finding connected tile groups using Kruskal's algorithm."""
        self.graph.update_all_tiles(self.tiles)
        forests = self.graph.kruskals_msf(self.tiles, max_weight=200)
        self.game.statistics['valid_sets_formed'] = len(forests)
        self.graph.print_forests(forests)
        
        # Reset all jokers first
        for tile_id, tile in self.tiles.items():
            if hasattr(tile, 'is_joker') and tile.is_joker:
                tile.reset_joker()
        
        # Update joker values in valid sets
        for forest in forests:
            tile_ids, _ = forest
            # Skip small groups (not valid sets)
            if len(tile_ids) < 3:
                continue
                
            # Get actual tiles from IDs
            forest_tiles = [self.tiles[t_id] for t_id in tile_ids]
            
            # Find jokers in this set
            jokers = [tile for tile in forest_tiles if hasattr(tile, 'is_joker') and tile.is_joker]
            if not jokers:
                continue
                
            # Get non-joker tiles to determine set type
            regular_tiles = [tile for tile in forest_tiles if not hasattr(tile, 'is_joker') or not tile.is_joker]
            if len(regular_tiles) < 2:  # Need at least 2 regular tiles to determine pattern
                continue
            
            # Determine set type and assign joker values
            if self.is_valid_group(forest_tiles):
                # In a group, all jokers get the same number as the group
                group_number = regular_tiles[0].number
                for joker in jokers:
                    joker.number = group_number
                    joker.in_set = True
                    
            elif self.is_valid_run(forest_tiles):
                # In a run, jokers fill in gaps or extend the sequence
                self._assign_joker_run_values(jokers, regular_tiles)

    def _assign_joker_run_values(self, jokers, regular_tiles):
        """
        Assign values to jokers in a run.
        
        Args:
            jokers: List of joker tiles in the set
            regular_tiles: List of non-joker tiles in the set
        """
        # Get the color and ordered numbers of the run
        color = regular_tiles[0].color
        numbers = sorted([t.number for t in regular_tiles])
        
        # Find gaps in the sequence
        min_num = min(numbers)
        max_num = max(numbers)
        full_sequence = set(range(min_num, max_num + 1))
        gaps = list(full_sequence - set(numbers))
        
        # Assign jokers to fill gaps first, then extend the sequence
        joker_index = 0
        
        # Step 1: Fill gaps
        for gap in sorted(gaps):
            if joker_index < len(jokers):
                jokers[joker_index].number = gap
                jokers[joker_index].in_set = True
                joker_index += 1
            else:
                break
        
        # Step 2: If we have remaining jokers, extend the sequence
        while joker_index < len(jokers):
            # Try to extend downward first, then upward
            if min_num > 1:
                min_num -= 1
                jokers[joker_index].number = min_num
                jokers[joker_index].in_set = True
            else:
                max_num += 1
                jokers[joker_index].number = max_num
                jokers[joker_index].in_set = True
            joker_index += 1

    def snap_tile(self, dropped_tile: Tile, snap_threshold: float = 200) -> None:
        """
        Snap dropped_tile horizontally so that it aligns to the left or right side
        of the nearest tile, creating a row.
        Assumes tile dimensions are 140px wide and 240px tall.
        """
        # Get the nearest neighbor info from the graph.
        nearest_id, nearest_distance = self.graph.get_nearest_neighbor(dropped_tile)
        if nearest_distance >= snap_threshold:
            return  # No snapping if too far away.
        
        nearest_tile = self.tiles.get(nearest_id)
        if not nearest_tile:
            return

        # Compute candidate positions:
        # Candidate to snap on the left side of nearest_tile:
        candidate_left = (nearest_tile.get_x() - dropped_tile.rect.width, nearest_tile.get_y())
        # Candidate to snap on the right side of nearest_tile:
        candidate_right = (nearest_tile.get_x() + nearest_tile.rect.width, nearest_tile.get_y())

        # Compute distance from the dropped tile's current position to each candidate.
        current_pos = dropped_tile.get_coordinates()
        dist_left = math.hypot(current_pos[0] - candidate_left[0],
                               current_pos[1] - candidate_left[1])
        dist_right = math.hypot(current_pos[0] - candidate_right[0],
                                current_pos[1] - candidate_right[1])

        # Choose the candidate with the smaller distance.
        best_candidate = candidate_left if dist_left < dist_right else candidate_right

        # Snap the dropped tile.
        dropped_tile.set_coordinates(best_candidate[0], best_candidate[1])
        # Update the graph for the dropped tile.
        self.graph.update_tile(dropped_tile)

    def validate_sets(self) -> bool:
        # Get the connected groups (forests) from the graph.
        forests = self.graph.kruskals_msf(self.tiles, max_weight=200)
        
        # Iterate over each forest and verify that it forms a valid set.
        for forest in forests:
            tile_ids, _ = forest
            tile_list = [self.tiles[t_id] for t_id in tile_ids]
            # A valid set must be either a valid group or a valid run.
            if not (self.is_valid_group(tile_list) or self.is_valid_run(tile_list)):
                # Print an error message with details about the invalid set.
                set_details = [f"(Number: {tile.number}, Color: {tile.color}{' Joker' if hasattr(tile, 'is_joker') and tile.is_joker else ''})"
                            for tile in tile_list]
                print("Invalid set:", set_details)
                return False

        # Clear the added_tiles list after validation.
        self.added_tiles = []
        return True

    def reset_board(self) -> None:
        # First, reset all tiles to their turn-start positions.
        for tile in self.tiles.values():
            tile.revert_to_turn_start()
        
        # Get the current player.
        current_player = self.game.players[self.game.current_turn]
        
        # Remove all tiles added this turn from the board.
        # We iterate over a copy because remove_tile modifies self.added_tiles.
        added_tile_ids = self.added_tiles.copy()
        for tile_id in added_tile_ids:
            tile = self.remove_tile(tile_id)
            if tile:
                # Return the tile to the current player's tile collection.
                current_player.add_tile(tile)
        
        # Finally, update the board's sets.
        self.update_sets()

    def get_tile_positions(self):
        tile_positions = {}
        for tile_id, tile in self.tiles.items(): 
            tile_positions[tile_id] = (tile.rect.x, tile.rect.y)
        return tile_positions