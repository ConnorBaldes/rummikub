# tests/unit/test_utils.py
import pytest
import numpy as np
from unittest.mock import MagicMock, patch
import sys
import io

from rummikub.utils import Graph

class TestGraph:
    """Unit tests for the Graph class in utils.py"""
    
    @pytest.fixture
    def mock_tile(self):
        """Create a configurable mock tile"""
        def _create_tile(tile_id, x, y):
            tile = MagicMock()
            tile.get_id.return_value = tile_id
            tile.get_x.return_value = x
            tile.get_y.return_value = y
            return tile
        return _create_tile
    
    @pytest.fixture
    def test_graph(self):
        """Create a graph for testing"""
        return Graph(max_size=10)
    
    def test_initialization(self, test_graph):
        """Test graph initialization"""
        # Check graph dimensions
        assert test_graph.size == 10
        assert test_graph.matrix.shape == (10, 10)
        assert test_graph.vertex_data.shape == (10, 3)
        
        # Check matrix initialization
        np.testing.assert_equal(np.diag(test_graph.matrix), np.zeros(10))
        assert np.all(test_graph.matrix[~np.eye(10, dtype=bool)] == np.inf)
        
        # Check vertex data initialization
        assert np.all(test_graph.vertex_data == -1)
    
    def test_add_tile(self, test_graph, mock_tile):
        """Test adding a tile to the graph"""
        # Create a tile at position (100, 200)
        tile1 = mock_tile(1, 100, 200)
        
        # Add the tile to the graph
        test_graph.add_tile(tile1)
        
        # Check vertex data was updated
        assert test_graph.vertex_data[1][0] == 100
        assert test_graph.vertex_data[1][1] == 200
        assert test_graph.vertex_data[1][2] == 1
        
        # Create a second tile at position (300, 400)
        tile2 = mock_tile(2, 300, 400)
        
        # Add the second tile
        test_graph.add_tile(tile2)
        
        # Check vertex data for second tile
        assert test_graph.vertex_data[2][0] == 300
        assert test_graph.vertex_data[2][1] == 400
        assert test_graph.vertex_data[2][2] == 2
        
        # Calculate expected distance
        expected_distance = np.sqrt((300-100)**2 + (400-200)**2)
        
        # Check distance matrix
        assert test_graph.matrix[1][2] == pytest.approx(expected_distance)
        assert test_graph.matrix[2][1] == pytest.approx(expected_distance)
    
    def test_update_tile(self, test_graph, mock_tile):
        """Test updating a tile's position"""
        # Add a tile to the graph
        tile1 = mock_tile(1, 100, 200)
        tile2 = mock_tile(2, 300, 400)
        
        test_graph.add_tile(tile1)
        test_graph.add_tile(tile2)
        
        # Update the position of tile1
        tile1 = mock_tile(1, 150, 250)
        test_graph.update_tile(tile1)
        
        # Check vertex data was updated
        assert test_graph.vertex_data[1][0] == 150
        assert test_graph.vertex_data[1][1] == 250
        
        # Calculate expected new distance
        expected_distance = np.sqrt((300-150)**2 + (400-250)**2)
        
        # Check distance matrix was updated
        assert test_graph.matrix[1][2] == pytest.approx(expected_distance)
        assert test_graph.matrix[2][1] == pytest.approx(expected_distance)
    
    def test_update_all_tiles(self, test_graph, mock_tile):
        """Test updating all tiles at once"""
        # Create tiles
        tile1 = mock_tile(1, 100, 200)
        tile2 = mock_tile(2, 300, 400)
        
        # Add tiles to graph
        test_graph.add_tile(tile1)
        test_graph.add_tile(tile2)
        
        # Create updated versions of tiles
        updated_tile1 = mock_tile(1, 150, 250)
        updated_tile2 = mock_tile(2, 350, 450)
        
        # Create dictionary of updated tiles
        tiles_dict = {1: updated_tile1, 2: updated_tile2}
        
        # Update all tiles
        test_graph.update_all_tiles(tiles_dict)
        
        # Check vertex data was updated
        assert test_graph.vertex_data[1][0] == 150
        assert test_graph.vertex_data[1][1] == 250
        assert test_graph.vertex_data[2][0] == 350
        assert test_graph.vertex_data[2][1] == 450
        
        # Calculate expected new distance
        expected_distance = np.sqrt((350-150)**2 + (450-250)**2)
        
        # Check distance matrix was updated
        assert test_graph.matrix[1][2] == pytest.approx(expected_distance)
        assert test_graph.matrix[2][1] == pytest.approx(expected_distance)
    
    def test_reset_tile_data(self, test_graph, mock_tile):
        """Test resetting a tile's data"""
        # Add a tile to the graph
        tile = mock_tile(1, 100, 200)
        test_graph.add_tile(tile)

        # Check tile was added
        assert test_graph.vertex_data[1][0] == 100

        # Reset the tile's data
        test_graph.reset_tile_data(1)

        # Check vertex data was reset
        assert np.all(test_graph.vertex_data[1] == -1)

        # Check distances were reset, accounting for diagonal element
        # Create expected array with all inf except diagonal
        expected = np.full(test_graph.matrix.shape[1], np.inf)
        expected[1] = 0  # Diagonal element is 0
        
        # Compare with actual matrix row
        assert np.array_equal(test_graph.matrix[1, :], expected)
    
    def test_remove_tile_by_id(self, test_graph, mock_tile):
        """Test removing a tile by ID"""
        # Add a tile to the graph
        tile = mock_tile(1, 100, 200)
        test_graph.add_tile(tile)
        
        # Remove the tile
        result = test_graph.remove_tile_by_id(1)
        
        # Check removal was successful
        assert result is True
        
        # Check vertex data was reset
        assert np.all(test_graph.vertex_data[1] == -1)
        
        # Try removing a non-existent tile
        result = test_graph.remove_tile_by_id(5)
        
        # Check removal failed
        assert result is False
    
    def test_get_nearest_neighbor(self, test_graph, mock_tile):
        """Test finding the nearest neighbor"""
        # Create three tiles with known distances
        tile1 = mock_tile(1, 100, 100)
        tile2 = mock_tile(2, 200, 200)  # Distance to tile1: 141.42
        tile3 = mock_tile(3, 130, 130)  # Distance to tile1: 42.43 (closest)
        
        # Add tiles to graph
        test_graph.add_tile(tile1)
        test_graph.add_tile(tile2)
        test_graph.add_tile(tile3)
        
        # Find nearest neighbor to tile1
        nearest_id, distance = test_graph.get_nearest_neighbor(tile1)
        
        # Check nearest neighbor is tile3
        assert nearest_id == 3
        assert distance == pytest.approx(42.43, abs=0.1)
        
        # Find nearest neighbor to tile2
        nearest_id, distance = test_graph.get_nearest_neighbor(tile2)
        
        # Check nearest neighbor is tile3
        assert nearest_id == 3
        assert distance == pytest.approx(98.99, abs=0.1)
    
    def test_kruskals_msf_single_component(self, test_graph, mock_tile):
        """Test Kruskal's algorithm with tiles close enough to form a single component"""
        # Create tiles in a cluster (all within 100 units)
        tile1 = mock_tile(1, 100, 100)
        tile2 = mock_tile(2, 150, 150)  # 70.7 units from tile1
        tile3 = mock_tile(3, 200, 100)  # 100 units from tile1, 70.7 from tile2
        
        # Add tiles to graph
        test_graph.add_tile(tile1)
        test_graph.add_tile(tile2)
        test_graph.add_tile(tile3)
        
        # Create tiles dictionary
        tiles_dict = {1: tile1, 2: tile2, 3: tile3}
        
        # Run Kruskal's algorithm with max_weight 100
        forests = test_graph.kruskals_msf(tiles_dict, 100)
        
        # Should have 1 component with all 3 vertices
        assert len(forests) == 1
        
        # Check the component contains all three vertices
        vertices, edges = forests[0]
        assert sorted(vertices) == [1, 2, 3]
        
        # Should have 2 edges
        assert len(edges) == 2
    
    def test_kruskals_msf_multiple_components(self, test_graph, mock_tile):
        """Test Kruskal's algorithm with tiles forming separate components"""
        # Create two clusters of tiles
        # Cluster 1
        tile1 = mock_tile(1, 100, 100)
        tile2 = mock_tile(2, 150, 150)  # 70.7 units from tile1
        
        # Cluster 2 (far from cluster 1)
        tile3 = mock_tile(3, 500, 500)
        tile4 = mock_tile(4, 550, 550)  # 70.7 units from tile3
        
        # Add tiles to graph
        test_graph.add_tile(tile1)
        test_graph.add_tile(tile2)
        test_graph.add_tile(tile3)
        test_graph.add_tile(tile4)
        
        # Create tiles dictionary
        tiles_dict = {1: tile1, 2: tile2, 3: tile3, 4: tile4}
        
        # Run Kruskal's algorithm with max_weight 100
        forests = test_graph.kruskals_msf(tiles_dict, 100)
        
        # Should have 2 components
        assert len(forests) == 2
        
        # Check components
        vertices_sets = [set(vertices) for vertices, _ in forests]
        assert {1, 2} in vertices_sets
        assert {3, 4} in vertices_sets
    
    def test_kruskals_msf_empty(self, test_graph):
        """Test Kruskal's algorithm with empty tiles dictionary"""
        # Run with empty dictionary
        forests = test_graph.kruskals_msf({}, 100)
        
        # Should return empty list
        assert forests == []
    
    def test_print_forests(self, test_graph, mock_tile, capsys):
        """Test printing forests"""
        # Set up a simple forest structure
        tile1 = mock_tile(1, 100, 100)
        tile2 = mock_tile(2, 150, 150)
        
        # Add tiles to graph
        test_graph.add_tile(tile1)
        test_graph.add_tile(tile2)
        
        # Create a forest manually
        forests = [([1, 2], [(1, 2, 70.71)])]
        
        # Capture stdout
        test_graph.print_forests(forests)
        captured = capsys.readouterr()
        
        # Check output contains expected strings
        assert "Active Sets:" in captured.out
        assert "[1, 2]" in captured.out