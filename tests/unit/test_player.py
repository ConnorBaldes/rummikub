# tests/unit/test_player.py
import pytest
from unittest.mock import MagicMock, patch
from rummikub.player import Player
from rummikub.tile import Tile

class TestPlayer:
    """Unit tests for the Player class"""
    
    @pytest.fixture
    def mock_game(self):
        """Create a mock game with a deck for testing"""
        game = MagicMock()
        game.deck = MagicMock()
        
        # Mock the deck to return a new tile when pick_tile is called
        def mock_pick_tile():
            mock_tile = MagicMock(spec=Tile)
            # Ensure each tile has a unique ID
            mock_tile.id = len(game.deck.pick_tile.mock_calls)
            mock_tile.get_id.return_value = mock_tile.id
            return mock_tile
        
        game.deck.pick_tile.side_effect = mock_pick_tile
        
        return game
    
    @pytest.fixture
    def test_player(self, mock_game):
        """Create a player instance for testing, with _build_rack patched"""
        with patch.object(Player, '_build_rack', return_value={}):
            player = Player(mock_game, "TestPlayer")
            return player
    
    def test_initialization(self, mock_game):
        """Test that player initializes correctly with proper initial values"""
        # Mock _build_rack to avoid side effects during initialization
        with patch.object(Player, '_build_rack', return_value={}):
            player = Player(mock_game, "TestPlayer")
            
            # Verify player properties
            assert player.game is mock_game
            assert player.name == "TestPlayer"
            assert player.tiles == {}
            assert player.initial_meld is False
            
            # Verify _build_rack was called during initialization
            Player._build_rack.assert_called_once()
    
    def test_build_rack(self, mock_game):
        """Test that _build_rack creates the correct initial hand"""
        # Create a player without patching _build_rack
        player = Player(mock_game, "TestPlayer")
        
        # Verify 14 tiles were drawn
        assert len(player.tiles) == 14
        
        # Verify the deck's pick_tile was called 14 times
        assert mock_game.deck.pick_tile.call_count == 14
        
        # Verify all tiles have unique IDs
        tile_ids = [tile.id for tile in player.tiles.values()]
        assert len(tile_ids) == len(set(tile_ids))  # All IDs should be unique
    
    def test_draw_tile(self, test_player, mock_game):
        """Test drawing a single tile from the deck"""
        # Record initial tile count
        initial_count = len(test_player.tiles)
        
        # Draw a tile
        test_player.draw_tile()
        
        # Verify a tile was added
        assert len(test_player.tiles) == initial_count + 1
        
        # Verify the deck's pick_tile method was called
        mock_game.deck.pick_tile.assert_called_once()
    
    def test_add_tile(self, test_player):
        """Test adding a tile to the player's hand"""
        # Create a mock tile
        mock_tile = MagicMock(spec=Tile)
        mock_tile.id = 999
        
        # Add the tile
        test_player.add_tile(mock_tile)
        
        # Verify the tile was added
        assert 999 in test_player.tiles
        assert test_player.tiles[999] is mock_tile
    
    def test_remove_tile_existing(self, test_player):
        """Test removing an existing tile from the player's hand"""
        # Create and add a mock tile
        mock_tile = MagicMock(spec=Tile)
        mock_tile.id = 999
        test_player.tiles[999] = mock_tile
        
        # Remove the tile
        removed_tile = test_player.remove_tile(999)
        
        # Verify the tile was removed
        assert 999 not in test_player.tiles
        assert removed_tile is mock_tile
    
    def test_remove_tile_nonexistent(self, test_player):
        """Test removing a nonexistent tile from the player's hand"""
        # Try to remove a tile that doesn't exist
        removed_tile = test_player.remove_tile(999)
        
        # Verify None was returned
        assert removed_tile is None
    
    def test_draw(self, test_player):
        """Test the draw method renders all tiles"""
        # Create mock tiles
        tile1 = MagicMock(spec=Tile)
        tile1.id = 1
        
        tile2 = MagicMock(spec=Tile)
        tile2.id = 2
        
        # Add tiles to player
        test_player.tiles = {
            1: tile1,
            2: tile2
        }
        
        # Create a mock screen
        mock_screen = MagicMock()
        
        # Call draw
        test_player.draw(mock_screen)
        
        # Verify each tile's draw method was called with the screen
        tile1.draw.assert_called_once_with(mock_screen)
        tile2.draw.assert_called_once_with(mock_screen)
    
    def test_initial_meld_tracking(self, test_player):
        """Test tracking the initial meld state"""
        # Initially false
        assert test_player.initial_meld is False
        
        # Set to true
        test_player.initial_meld = True
        assert test_player.initial_meld is True
        
        # Set back to false
        test_player.initial_meld = False
        assert test_player.initial_meld is False
    
    def test_rack_emptying(self, test_player):
        """Test removing all tiles from a player's rack"""
        # Add some mock tiles
        for i in range(3):
            mock_tile = MagicMock(spec=Tile)
            mock_tile.id = i
            test_player.tiles[i] = mock_tile
        
        # Verify we have 3 tiles
        assert len(test_player.tiles) == 3
        
        # Remove all tiles
        for i in range(3):
            test_player.remove_tile(i)
        
        # Verify the rack is empty
        assert len(test_player.tiles) == 0