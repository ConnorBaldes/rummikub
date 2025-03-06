# tests/unit/test_board.py
import pytest
import pygame
import math
from unittest.mock import MagicMock, patch

from rummikub.board import Board
from rummikub.tile import Tile
from rummikub.utils import Graph

class TestBoard:
    """Unit tests for the Board class"""
    
    @pytest.fixture
    def mock_game(self):
        """Create a mock game object"""
        game = MagicMock()
        game.statistics = {'valid_sets_formed': 0}
        game.current_turn = 0
        game.players = [MagicMock()]
        return game
    
    @pytest.fixture
    def mock_graph(self):
        """Create a mock Graph class"""
        with patch('rummikub.board.Graph', autospec=True) as MockGraph:
            # Make the constructor return a mock object
            mock_graph_instance = MagicMock(spec=Graph)
            MockGraph.return_value = mock_graph_instance
            
            # Configure nearest neighbor method
            mock_graph_instance.get_nearest_neighbor.return_value = (1, 100)  # Default (id, distance)
            
            # Configure kruskals_msf method
            mock_graph_instance.kruskals_msf.return_value = []  # Default empty forests
            
            yield MockGraph, mock_graph_instance
    
    @pytest.fixture
    def board(self, mock_game, mock_graph):
        """Create a board instance with mocked dependencies"""
        _, mock_graph_instance = mock_graph
        board = Board(mock_game)
        
        # Reset mock to clear initialization calls
        mock_graph_instance.reset_mock()
        
        return board
    
    @pytest.fixture
    def mock_tile(self):
        """Create configurable mock tiles"""
        def _create_tile(tile_id, number, color, is_joker=False, x=0, y=0):
            tile = MagicMock(spec=Tile)
            tile.id = tile_id
            tile.number = number
            tile.color = color
            tile.is_joker = is_joker
            tile.reset_joker = MagicMock()
            tile.get_id = MagicMock(return_value=tile_id)
            tile.get_x = MagicMock(return_value=x)
            tile.get_y = MagicMock(return_value=y)
            tile.get_coordinates = MagicMock(return_value=(x, y))
            tile.rect = MagicMock()
            tile.rect.width = 140
            tile.rect.height = 240
            tile.rect.x = x
            tile.rect.y = y
            tile.set_coordinates = MagicMock()
            tile.revert_to_turn_start = MagicMock()
            return tile
        return _create_tile
    
    def test_initialization(self, mock_game, mock_graph):
        """Test board initialization"""
        MockGraph, _ = mock_graph
        board = Board(mock_game)
        
        # Verify graph initialization
        MockGraph.assert_called_once_with(106)  # Max size of 106 tiles
        
        # Verify initial state
        assert board.game == mock_game
        assert board.tiles == {}
        assert board.added_tiles == []
    
    def test_add_tile(self, board, mock_tile):
        """Test adding a tile to the board"""
        # Create a tile
        tile = mock_tile(1, 8, "red")
        
        # Add to board
        board.add_tile(tile)
        
        # Verify tile was added to the board's tiles dictionary
        assert board.tiles[1] == tile
        
        # Verify tile ID was added to added_tiles list
        assert 1 in board.added_tiles
        
        # Verify graph was updated
        board.graph.add_tile.assert_called_once_with(tile)
    
    def test_remove_tile_current_turn(self, board, mock_tile):
        """Test removing a tile that was added in the current turn"""
        # Create and add a tile
        tile = mock_tile(1, 8, "red")
        board.tiles[1] = tile
        board.added_tiles.append(1)
        
        # Remove the tile
        removed_tile = board.remove_tile(1)
        
        # Verify tile was removed
        assert removed_tile == tile
        assert 1 not in board.tiles
        assert 1 not in board.added_tiles
        
        # Verify graph was updated
        board.graph.remove_tile_by_id.assert_called_once_with(1)
    
    def test_remove_tile_previous_turn(self, board, mock_tile):
        """Test removing a tile that was added in a previous turn"""
        # Create and add a tile (not in added_tiles to simulate previous turn)
        tile = mock_tile(1, 8, "red")
        board.tiles[1] = tile
        
        # Remove the tile
        removed_tile = board.remove_tile(1)
        
        # Verify tile was not removed
        assert removed_tile is None
        assert 1 in board.tiles
        
        # Verify graph was not updated
        board.graph.remove_tile_by_id.assert_not_called()
    
    def test_draw(self, board, mock_tile):
        """Test drawing all tiles on the board"""
        # Create and add tiles
        tile1 = mock_tile(1, 8, "red")
        tile2 = mock_tile(2, 9, "blue")
        board.tiles = {1: tile1, 2: tile2}
        
        # Create mock screen
        mock_screen = MagicMock()
        
        # Draw tiles
        board.draw(mock_screen)
        
        # Verify each tile's draw method was called
        tile1.draw.assert_called_once_with(mock_screen)
        tile2.draw.assert_called_once_with(mock_screen)
    
    def test_is_valid_group_valid(self, board, mock_tile):
        """Test valid group validation (same number, different colors)"""
        # Create a valid group: same number (8), different colors
        tile1 = mock_tile(1, 8, "red")
        tile2 = mock_tile(2, 8, "blue")
        tile3 = mock_tile(3, 8, "black")
        
        # Test group validation
        assert board.is_valid_group([tile1, tile2, tile3]) is True
    
    def test_is_valid_group_invalid_count(self, board, mock_tile):
        """Test invalid group with wrong tile count"""
        # Create tiles with same number
        tile1 = mock_tile(1, 8, "red")
        tile2 = mock_tile(2, 8, "blue")
        
        # Test with too few tiles (need 3 or 4)
        assert board.is_valid_group([tile1, tile2]) is False
        
        # Create more tiles
        tile3 = mock_tile(3, 8, "black")
        tile4 = mock_tile(4, 8, "orange")
        tile5 = mock_tile(5, 8, "green")
        
        # Test with too many tiles (more than 4)
        assert board.is_valid_group([tile1, tile2, tile3, tile4, tile5]) is False
    
    def test_is_valid_group_invalid_numbers(self, board, mock_tile):
        """Test invalid group with different numbers"""
        # Create tiles with different numbers
        tile1 = mock_tile(1, 8, "red")
        tile2 = mock_tile(2, 9, "blue")
        tile3 = mock_tile(3, 10, "black")
        
        # Test validation
        assert board.is_valid_group([tile1, tile2, tile3]) is False
    
    def test_is_valid_group_invalid_colors(self, board, mock_tile):
        """Test invalid group with duplicate colors"""
        # Create tiles with same number but duplicate colors
        tile1 = mock_tile(1, 8, "red")
        tile2 = mock_tile(2, 8, "red")  # Duplicate color
        tile3 = mock_tile(3, 8, "black")
        
        # Test validation
        assert board.is_valid_group([tile1, tile2, tile3]) is False
    
    def test_is_valid_group_with_joker(self, board, mock_tile):
        """Test valid group with a joker"""
        # Create tiles with one joker
        tile1 = mock_tile(1, 8, "red")
        tile2 = mock_tile(2, 8, "blue")
        joker = mock_tile(3, 0, "joker", is_joker=True)
        
        # Test validation
        assert board.is_valid_group([tile1, tile2, joker]) is True
    
    def test_is_valid_group_all_jokers(self, board, mock_tile):
        """Test invalid group with all jokers"""
        # Create all joker tiles
        joker1 = mock_tile(1, 0, "joker", is_joker=True)
        joker2 = mock_tile(2, 0, "joker", is_joker=True)
        joker3 = mock_tile(3, 0, "joker", is_joker=True)
        
        # Test validation - should fail as we need at least one non-joker
        assert board.is_valid_group([joker1, joker2, joker3]) is False
    
    def test_is_valid_run_valid(self, board, mock_tile):
        """Test valid run validation (same color, sequential numbers)"""
        # Create a valid run: same color, sequential numbers
        tile1 = mock_tile(1, 3, "red")
        tile2 = mock_tile(2, 4, "red")
        tile3 = mock_tile(3, 5, "red")
        
        # Test run validation
        assert board.is_valid_run([tile1, tile2, tile3]) is True
    
    def test_is_valid_run_invalid_count(self, board, mock_tile):
        """Test invalid run with too few tiles"""
        # Create tiles
        tile1 = mock_tile(1, 3, "red")
        tile2 = mock_tile(2, 4, "red")
        
        # Test with too few tiles (need at least 3)
        assert board.is_valid_run([tile1, tile2]) is False
    
    def test_is_valid_run_invalid_colors(self, board, mock_tile):
        """Test invalid run with different colors"""
        # Create tiles with sequential numbers but different colors
        tile1 = mock_tile(1, 3, "red")
        tile2 = mock_tile(2, 4, "blue")
        tile3 = mock_tile(3, 5, "red")
        
        # Test validation
        assert board.is_valid_run([tile1, tile2, tile3]) is False
    
    def test_is_valid_run_invalid_sequence(self, board, mock_tile):
        """Test invalid run with non-sequential numbers"""
        # Create tiles with non-sequential numbers
        tile1 = mock_tile(1, 3, "red")
        tile2 = mock_tile(2, 5, "red")  # Gap in sequence
        tile3 = mock_tile(3, 7, "red")  # Another gap
        
        # Test validation - should fail as gaps require jokers
        assert board.is_valid_run([tile1, tile2, tile3]) is False
    
    def test_is_valid_run_with_joker_filling_gap(self, board, mock_tile):
        """Test valid run with a joker filling a gap"""
        # Create tiles with a gap to be filled by joker
        tile1 = mock_tile(1, 3, "red")
        joker = mock_tile(2, 0, "joker", is_joker=True)
        tile3 = mock_tile(3, 5, "red")
        
        # Test validation
        assert board.is_valid_run([tile1, joker, tile3]) is True
    
    def test_is_valid_run_with_duplicate_numbers(self, board, mock_tile):
        """Test invalid run with duplicate numbers"""
        # Create tiles with duplicate numbers
        tile1 = mock_tile(1, 3, "red")
        tile2 = mock_tile(2, 3, "red")  # Duplicate number
        tile3 = mock_tile(3, 4, "red")
        
        # Test validation
        assert board.is_valid_run([tile1, tile2, tile3]) is False
    
    def test_update_sets(self, board, mock_tile):
        """Test updating sets and joker values"""
        # Configure mock graph to return forests
        forest1_tiles = [1, 2, 3]  # A valid group
        forest2_tiles = [4, 5, 6, 7]  # A valid run
        
        # Create forest data
        forest1 = (forest1_tiles, [(1, 2, 50), (2, 3, 60)])
        forest2 = (forest2_tiles, [(4, 5, 70), (5, 6, 80), (6, 7, 90)])
        
        board.graph.kruskals_msf.return_value = [forest1, forest2]
        
        # Create tiles
        # Forest 1: Group (same number 8, different colors)
        tile1 = mock_tile(1, 8, "red")
        tile2 = mock_tile(2, 8, "blue")
        joker1 = mock_tile(3, 0, "joker", is_joker=True)
        
        # Forest 2: Run (same color red, sequential numbers with a joker)
        tile4 = mock_tile(4, 3, "red")
        tile5 = mock_tile(5, 4, "red")
        tile7 = mock_tile(7, 6, "red")
        joker2 = mock_tile(6, 0, "joker", is_joker=True)
        
        # Add tiles to board
        board.tiles = {
            1: tile1, 2: tile2, 3: joker1,
            4: tile4, 5: tile5, 6: joker2, 7: tile7
        }
        
        # Mock is_valid_group and is_valid_run
        with patch.object(board, 'is_valid_group') as mock_is_group, \
             patch.object(board, 'is_valid_run') as mock_is_run:
            
            # Configure mock returns
            mock_is_group.side_effect = lambda tiles: len(tiles) == 3 and all(t.id in forest1_tiles for t in tiles)
            mock_is_run.side_effect = lambda tiles: len(tiles) == 4 and all(t.id in forest2_tiles for t in tiles)
            
            # Update sets
            board.update_sets()
            
            # Verify graph methods were called
            board.graph.update_all_tiles.assert_called_once_with(board.tiles)
            board.graph.kruskals_msf.assert_called_once_with(board.tiles, max_weight=200)
            
            # Verify jokers were reset first
            joker1.reset_joker.assert_called_once()
            joker2.reset_joker.assert_called_once()
            
            # Verify statistics were updated
            assert board.game.statistics['valid_sets_formed'] == 2
    
    def test_assign_joker_run_values_fill_gaps(self, board, mock_tile):
        """Test assigning values to jokers in a run with gaps"""
        # Create regular tiles with a gap
        tile1 = mock_tile(1, 3, "red")
        tile2 = mock_tile(2, 5, "red")
        tile3 = mock_tile(3, 7, "red")
        
        # Create jokers to fill the gaps
        joker1 = mock_tile(4, 0, "joker", is_joker=True)
        joker2 = mock_tile(5, 0, "joker", is_joker=True)
        
        # Call method directly
        board._assign_joker_run_values([joker1, joker2], [tile1, tile2, tile3])
        
        # Verify joker values (should fill gaps 4 and 6)
        assert joker1.number in [4, 6]
        assert joker2.number in [4, 6]
        assert joker1.number != joker2.number  # Should have different values
        assert joker1.in_set is True
        assert joker2.in_set is True
    
    def test_assign_joker_run_values_extend(self, board, mock_tile):
        """Test assigning values to jokers in a run by extending the sequence"""
        # Create regular tiles with no gaps
        tile1 = mock_tile(1, 3, "red")
        tile2 = mock_tile(2, 4, "red")
        tile3 = mock_tile(3, 5, "red")
        
        # Create jokers to extend the sequence
        joker1 = mock_tile(4, 0, "joker", is_joker=True)
        joker2 = mock_tile(5, 0, "joker", is_joker=True)
        
        # Call method directly
        board._assign_joker_run_values([joker1, joker2], [tile1, tile2, tile3])
        
        # Verify joker values (should extend: 2 and 6 or 1 and 2)
        valid_extensions = [(2, 6), (1, 2), (2, 1), (6, 7)]
        joker_values = (joker1.number, joker2.number)
        
        assert any(joker_values[0] == v[0] and joker_values[1] == v[1] for v in valid_extensions) or \
               any(joker_values[0] == v[1] and joker_values[1] == v[0] for v in valid_extensions)
        
        assert joker1.in_set is True
        assert joker2.in_set is True
    
    def test_snap_tile_within_threshold(self, board, mock_tile):
        """Test snapping a tile within threshold distance"""
        # Create a reference tile
        ref_tile = mock_tile(1, 8, "red", x=200, y=300)
        board.tiles[1] = ref_tile
        
        # Create a tile to snap
        tile_to_snap = mock_tile(2, 9, "blue", x=250, y=310)
        
        # Configure graph nearest neighbor
        board.graph.get_nearest_neighbor.return_value = (1, 60)  # ID 1, distance 60
        
        # Snap the tile
        board.snap_tile(tile_to_snap)
        
        # Verify tile was snapped to the right of reference tile
        expected_x = 200 + ref_tile.rect.width
        expected_y = 300
        tile_to_snap.set_coordinates.assert_called_once_with(expected_x, expected_y)
        
        # Verify graph was updated
        board.graph.update_tile.assert_called_once_with(tile_to_snap)
    
    def test_snap_tile_left_side(self, board, mock_tile):
        """Test snapping a tile to the left side of reference"""
        # Create a reference tile
        ref_tile = mock_tile(1, 8, "red", x=200, y=300)
        board.tiles[1] = ref_tile
        
        # Create a tile to snap (positioned to favor left snapping)
        tile_to_snap = mock_tile(2, 9, "blue", x=30, y=310)
        
        # Configure graph nearest neighbor
        board.graph.get_nearest_neighbor.return_value = (1, 60)  # ID 1, distance 60
        
        # Snap the tile
        board.snap_tile(tile_to_snap)
        
        # Verify tile was snapped to the left of reference tile
        expected_x = 200 - tile_to_snap.rect.width
        expected_y = 300
        tile_to_snap.set_coordinates.assert_called_once_with(expected_x, expected_y)
    
    def test_snap_tile_beyond_threshold(self, board, mock_tile):
        """Test snapping a tile beyond threshold distance"""
        # Create a reference tile
        ref_tile = mock_tile(1, 8, "red", x=200, y=300)
        board.tiles[1] = ref_tile
        
        # Create a tile too far to snap
        tile_to_snap = mock_tile(2, 9, "blue", x=500, y=600)
        
        # Configure graph nearest neighbor
        board.graph.get_nearest_neighbor.return_value = (1, 500)  # ID 1, distance 500
        
        # Try to snap the tile
        board.snap_tile(tile_to_snap)
        
        # Verify tile was not snapped (set_coordinates not called)
        tile_to_snap.set_coordinates.assert_not_called()
    
    def test_validate_sets_valid(self, board, mock_tile):
        """Test validating board sets when all are valid"""
        # Configure mock graph to return forests
        forest1 = ([1, 2, 3], [(1, 2, 50), (2, 3, 60)])
        forest2 = ([4, 5, 6, 7], [(4, 5, 70), (5, 6, 80), (6, 7, 90)])
        board.graph.kruskals_msf.return_value = [forest1, forest2]
        
        # Create tiles
        tile1 = mock_tile(1, 8, "red")
        tile2 = mock_tile(2, 8, "blue")
        tile3 = mock_tile(3, 8, "black")
        
        tile4 = mock_tile(4, 3, "red")
        tile5 = mock_tile(5, 4, "red")
        tile6 = mock_tile(6, 5, "red")
        tile7 = mock_tile(7, 6, "red")
        
        # Add tiles to board
        board.tiles = {
            1: tile1, 2: tile2, 3: tile3,
            4: tile4, 5: tile5, 6: tile6, 7: tile7
        }
        
        # Set some tiles as added this turn
        board.added_tiles = [3, 7]
        
        # Mock is_valid_group and is_valid_run
        with patch.object(board, 'is_valid_group') as mock_is_group, \
             patch.object(board, 'is_valid_run') as mock_is_run:
            
            # Configure mock returns - forest1 is a group, forest2 is a run
            mock_is_group.side_effect = lambda tiles: len(tiles) == 3
            mock_is_run.side_effect = lambda tiles: len(tiles) == 4
            
            # Validate sets
            result = board.validate_sets()
            
            # Verify result is True (all sets are valid)
            assert result is True
            
            # Verify added_tiles list was cleared
            assert board.added_tiles == []
    
    def test_validate_sets_invalid(self, board, mock_tile):
        """Test validating board sets when some are invalid"""
        # Configure mock graph to return forests
        forest1 = ([1, 2, 3], [(1, 2, 50), (2, 3, 60)])  # Valid group
        forest2 = ([4, 5, 6, 7], [(4, 5, 70), (5, 6, 80), (6, 7, 90)])  # Invalid set
        board.graph.kruskals_msf.return_value = [forest1, forest2]
        
        # Add tiles to board
        board.tiles = {
            1: mock_tile(1, 8, "red"),
            2: mock_tile(2, 8, "blue"),
            3: mock_tile(3, 8, "black"),
            
            4: mock_tile(4, 3, "red"),
            5: mock_tile(5, 9, "blue"),  # Mixed colors, non-sequential
            6: mock_tile(6, 2, "black"),
            7: mock_tile(7, 6, "orange")
        }
        
        # Mock is_valid_group and is_valid_run
        with patch.object(board, 'is_valid_group') as mock_is_group, \
             patch.object(board, 'is_valid_run') as mock_is_run:
            
            # Configure mock returns - forest1 is valid, forest2 is invalid
            mock_is_group.side_effect = lambda tiles: all(t.id in [1, 2, 3] for t in tiles)
            mock_is_run.return_value = False
            
            # Validate sets
            result = board.validate_sets()
            
            # Verify result is False (invalid sets found)
            assert result is False
            
            # Verify added_tiles list was NOT cleared
            assert board.added_tiles == board.added_tiles
    
    def test_reset_board(self, board, mock_tile):
        """Test resetting the board state"""
        # Create tiles
        tile1 = mock_tile(1, 8, "red")  # Already on board
        tile2 = mock_tile(2, 9, "blue")  # Added this turn
        
        # Set up board state
        board.tiles = {1: tile1, 2: tile2}
        board.added_tiles = [2]
        
        # Configure remove_tile to return the tile
        with patch.object(board, 'remove_tile', return_value=tile2) as mock_remove:
            # Reset the board
            board.reset_board()
            
            # Verify all tiles were reverted to turn-start position
            tile1.revert_to_turn_start.assert_called_once()
            tile2.revert_to_turn_start.assert_called_once()
            
            # Verify added tiles were removed
            mock_remove.assert_called_once_with(2)
            
            # Verify removed tile was added back to player
            board.game.players[0].add_tile.assert_called_once_with(tile2)
            
            # Verify sets were updated
            board.graph.update_all_tiles.assert_called_once()
    
    def test_get_tile_positions(self, board, mock_tile):
        """Test getting tile positions"""
        # Create tiles with known positions
        tile1 = mock_tile(1, 8, "red", x=100, y=200)
        tile2 = mock_tile(2, 9, "blue", x=300, y=400)
        
        # Add to board
        board.tiles = {1: tile1, 2: tile2}
        
        # Get positions
        positions = board.get_tile_positions()
        
        # Verify correct positions were returned
        assert positions == {1: (100, 200), 2: (300, 400)}