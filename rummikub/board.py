class Board:
    def __init__(self):
        self.sets = []

    def add_set(self, tile_set):
        # Validate and add a new set
        if not self.is_valid_set(tile_set):
            raise ValueError("Invalid tile set")
        self.sets.append(tile_set)


    def is_valid_set(self, tile_set):
        """
        Check if a tile set is valid (run or group).
        :param tile_set: A list of Tile objects.
        :return: True if the set is valid, False otherwise.
        """
        if len(tile_set) < 3:
            return False  # Sets must have at least 3 tiles

        # Check for a "group": same number, different colors
        if self._is_group(tile_set):
            return True


        # Check for a "run": consecutive numbers, same color
        if self._is_run(tile_set):
            return True

        return False

    def _is_group(self, tile_set):
        """
        Check if the tile set is a valid group (same number, different colors).
        :param tile_set: A list of Tile objects.
        :return: True if the set is a valid group, False otherwise.
        """
        numbers = {tile.number for tile in tile_set if not tile.is_joker}
        colors = {tile.color for tile in tile_set if not tile.is_joker}

        # All tiles must have the same number and unique colors (ignoring jokers)
        return len(numbers) == 1 and len(colors) == len(tile_set) - sum(tile.is_joker for tile in tile_set)

    def _is_run(self, tile_set):
        """
        Check if the tile set is a valid run (consecutive numbers, same color).
        :param tile_set: A list of Tile objects.
        :return: True if the set is a valid run, False otherwise.
        """
        # Separate tiles into regular tiles (with numbers) and joker tiles (with None)
        regular_tiles = [tile for tile in tile_set if not tile.is_joker]
        joker_tiles = [tile for tile in tile_set if tile.is_joker]
        
        # Check for duplicates in the regular tiles
        if len(regular_tiles) != len(set(regular_tiles)):
            return False  # There are duplicate tiles, so it's not a valid run
        
        # Sort regular tiles by number
        sorted_tiles = sorted(regular_tiles, key=lambda tile: tile.number)
        
        # Ensure all tiles in the run have the same color, ignoring joker tiles
        colors = {tile.color for tile in sorted_tiles}
        
        if len(colors) != 1:
            return False  # All tiles must have the same color in a run
        
        # Check for consecutive numbers in the sorted regular tiles
        consecutive = True
        missing_numbers = []
        
        for i in range(1, len(sorted_tiles)):
            # If the numbers are not consecutive, note the missing numbers
            if sorted_tiles[i].number != sorted_tiles[i-1].number + 1:
                consecutive = False
                # Add the missing numbers between the current and previous tile
                missing_numbers.extend(range(sorted_tiles[i-1].number + 1, sorted_tiles[i].number))
        
        # If the sequence is not consecutive, we need to check if jokers can fill the gaps
        if not consecutive:
            if len(missing_numbers) > len(joker_tiles):
                return False  # Not enough jokers to fill the gaps
            # If there are enough jokers, they can fill the missing numbers
            joker_tiles_needed = len(missing_numbers)
            if joker_tiles_needed <= len(joker_tiles):
                return True  # The run can be completed with the jokers
            return False

        # If the tiles were already consecutive, the run is valid
        return True


        
    def __repr__(self):
        """
        String representation of the board for debugging.
        :return: A string describing the board's current state.
        """
        return f"Board({self.sets})"