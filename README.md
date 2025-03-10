# Rummikub Game Implementation

A comprehensive implementation of the classic Rummikub tile game built with Python and Pygame.
![Rummikub implementation game play](./readme_images/rummikub_gameplay.png)

## Game Overview

Rummikub challenges players to strategically place tiles in valid combinations, aiming to be the first to empty their rack. This implementation delivers an authentic digital experience with intuitive drag-and-drop mechanics, automatic rule validation, and a polished interface.

**Objective:** Be the first player to play all tiles from your rack by forming them into valid sets and runs.


<h3 align="center">Tiles</h3>

<table align="center">
    <tr>
        <th align="center" width="20%"><pre>Red (1-13)</pre></th>
        <th align="center" width="20%"><pre>Blue (1-13)</pre></th>
        <th align="center" width="20%"><pre>Black (1-13)</pre></th>
        <th align="center" width="20%"><pre>Orange (1-13)</pre></th>
        <th align="center" width="20%"><pre>Jokers</pre></th>
    </tr>
    <tr>
        <td align="center"><img src="./rummikub/assets/tiles_2/tile_1_red.png" width="40" alt="Red 1"></td>
        <td align="center"><img src="./rummikub/assets/tiles_2/tile_1_blue.png" width="40" alt="Blue 1"></td>
        <td align="center"><img src="./rummikub/assets/tiles_2/tile_1_black.png" width="40" alt="Black 1"></td>
        <td align="center"><img src="./rummikub/assets/tiles_2/tile_1_orange.png" width="40" alt="Orange 1"></td>
        <td align="center"><img src="./rummikub/assets/tiles_2/tile_joker_1.png" width="40" alt="Joker 1"></td>
    </tr>
    <tr>
        <td align="center"><img src="./rummikub/assets/tiles_2/tile_2_red.png" width="40" alt="Red 5"></td>
        <td align="center"><img src="./rummikub/assets/tiles_2/tile_2_blue.png" width="40" alt="Blue 5"></td>
        <td align="center"><img src="./rummikub/assets/tiles_2/tile_2_black.png" width="40" alt="Black 5"></td>
        <td align="center"><img src="./rummikub/assets/tiles_2/tile_2_orange.png" width="40" alt="Orange 5"></td>
        <td align="center"><img src="./rummikub/assets/tiles_2/tile_joker_2.png" width="40" alt="Joker 2"></td>
    </tr>
    <tr>
        <td align="center"><img src="./rummikub/assets/tiles_2/tile_3_red.png" width="40" alt="Red 9"></td>
        <td align="center"><img src="./rummikub/assets/tiles_2/tile_3_blue.png" width="40" alt="Blue 9"></td>
        <td align="center"><img src="./rummikub/assets/tiles_2/tile_3_black.png" width="40" alt="Black 9"></td>
        <td align="center"><img src="./rummikub/assets/tiles_2/tile_3_orange.png" width="40" alt="Orange 9"></td>
        <td align="center"></td>
    </tr>
    <tr>
        <td align="center"><img src="./rummikub/assets/tiles_2/tile_4_red.png" width="40" alt="Red 13"></td>
        <td align="center"><img src="./rummikub/assets/tiles_2/tile_4_blue.png" width="40" alt="Blue 13"></td>
        <td align="center"><img src="./rummikub/assets/tiles_2/tile_4_black.png" width="40" alt="Black 13"></td>
        <td align="center"><img src="./rummikub/assets/tiles_2/tile_4_orange.png" width="40" alt="Orange 13"></td>
        <td align="center"></td>
    </tr>
</table>

<table align="center" width="100%">
    <tr>
        <th width="50%" align="center" >Valid Groups</th>
        <th width="50%" align="center" >Valid Runs</th>
    </tr>
    <tr>
        <td align="center">
            <p><pre>Same number in different colors (3-4 tiles)</pre></p>
            <img src="./rummikub/assets/tiles_2/tile_7_orange.png" width="40">
            <img src="./rummikub/assets/tiles_2/tile_7_blue.png" width="40">
            <img src="./rummikub/assets/tiles_2/tile_7_red.png" width="40">
            <br><br>
            <img src="./rummikub/assets/tiles_2/tile_4_orange.png" width="40">
            <img src="./rummikub/assets/tiles_2/tile_4_red.png" width="40">
            <img src="./rummikub/assets/tiles_2/tile_4_blue.png" width="40">
            <img src="./rummikub/assets/tiles_2/tile_4_black.png" width="40">
        </td>
        <td align="center">
            <p><pre>Consecutive numbers in same color (3+ tiles)</pre></p>
            <img src="./rummikub/assets/tiles_2/tile_7_red.png" width="40">
            <img src="./rummikub/assets/tiles_2/tile_8_red.png" width="40">
            <img src="./rummikub/assets/tiles_2/tile_9_red.png" width="40">
            <br><br>
            <img src="./rummikub/assets/tiles_2/tile_3_blue.png" width="40">
            <img src="./rummikub/assets/tiles_2/tile_4_blue.png" width="40">
            <img src="./rummikub/assets/tiles_2/tile_5_blue.png" width="40">
            <img src="./rummikub/assets/tiles_2/tile_6_blue.png" width="40">
        </td>
    </tr>
</table>

<table width="100%">
    <tr>
        <th width="30%" align="center" >Initial Meld</th>
        <th width="40%" align="center" >Manipulation</th>
        <th width="30%" align="center" >Jokers & Winning</th>
    </tr>
    <tr>
        <td width="30%" valign="top" align="left">
            <p>Players must start with a meld totaling at least <strong>30 points</strong> from their rack.</p>
            <p>Example: <br>9+10+11=30 (Blue run)<br>
            <img src="./rummikub/assets/tiles_2/tile_9_blue.png" width="30">
            <img src="./rummikub/assets/tiles_2/tile_10_blue.png" width="30">
            <img src="./rummikub/assets/tiles_2/tile_11_blue.png" width="30">
            </p>
        </td>
        <td width="40%" valign="top" align="left">
            <p>After initial meld, players can:</p>
            <p>
                • Add tiles from rack to existing sets<br>
                • Rearrange table tiles to form new sets<br>
                • Split runs into smaller valid runs<br>
                • Combine sets into new arrangements
            </p>
        </td>
        <td width="30%" valign="top" align="left">
            <p><strong>Jokers:</strong> Substitute for any tile. Can be retrieved by replacing with the actual tile it represents.</p>
            <p><strong>Winning:</strong> First to play all tiles wins. Score equals sum of opponents' remaining tile values.</p>
        </td>
    </tr>
</table>

<br>

## Installation

### Using Conda (Recommended)

```bash
# Clone the repository
git clone https://github.com/ConnorBaldes/rummikub.git
cd rummikub

# Create the conda environment
conda env create -f environment.yaml

# Activate the environment
conda activate rummikub
```

### Using Pip
```bash
# Clone the repository
git clone https://github.com/ConnorBaldes/rummikub.git
cd rummikub

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

<br>

## Running the Game
```bash
python main.py
```
The game will initialize and display the main menu where you can start a new game, adjust settings, or view instructions.

<br>

## Testing
This project uses pytest for unit testing, integration testing, and functional testing. The test suite ensures the game components work correctly individually and together.

### Test Structure
Tests are organized into the following directories:
- tests/unit/: Contains unit tests for individual components
- tests/integration/: Contains tests that verify multiple components work together
- tests/functional/: Contains functional tests for higher-level game behavior

### Running Tests
```bash
# You can run the entire test suite with:
python run_tests.py

# Or use pytest directly:
pytest

# To run a specific test file:
pytest tests/unit/test_tile.py

# To run a specific test:
pytest tests/unit/test_tile.py::TestTile::test_resize_image
```

### Test Coverage
```bash
# Run the tests with coverage:
pytest --cov=rummikub

# Generate an HTML coverage report:
pytest --cov=rummikub --cov-report=html
```
Then open htmlcov/index.html in your browser to view the report.

<br>

# Technical Architecture & Design

<blockquote>
    <h3>Core Architecture (MVC Pattern)</h3>
    <ul>
        <li><strong>Model:</strong> Game state management (Board, Player, Tile classes)</li>
        <li><strong>View:</strong> Rendering and display logic (GameScreen, ThemeManager)</li>
        <li><strong>Controller:</strong> Game flow and logic coordination (Game class)</li>
    </ul>
</blockquote>

<table width="100%">
    <tr>
        <th align="center" width="50%"><h3>Implementation Highlights</h3></th>
        <th align="center" width="50%"><h3>Design Patterns</h3></th>
    </tr>
    <tr valign="top">
        <td>
            <ul>
                <li><strong>Optimized Algorithms:</strong> NumPy-powered matrix operations for efficiency</li>
                <li><strong>State Preservation:</strong> Robust game state tracking between turns</li>
                <li><strong>Error Handling:</strong> Graceful recovery from invalid moves with clear feedback</li>
                <li><strong>Type Annotations:</strong> Comprehensive Python type hints for improved code clarity</li>
                <li><strong>Duck Typing:</strong> Flexible object interfaces following Pythonic principles</li>
            </ul>
        </td>
        <td>
            <ul>
                <li><strong>Singleton Pattern:</strong> ThemeManager ensures consistent styling</li>
                <li><strong>Factory Pattern:</strong> Deck class produces tiles with standardized properties</li>
                <li><strong>State Pattern:</strong> Screen manager handles transitions between game states</li>
                <li><strong>Observer Pattern:</strong> Event system for notifications and UI updates</li>
            </ul>
        </td>
    </tr>
</table>

### System Design
The Rummikub game is built with a structured, object-oriented architecture using Python and Pygame. The system separates game logic from rendering concerns and employs several design patterns to maintain clean, maintainable code.
![System architecture image](./readme_images/system_architecture.png)


### Directory Structure

<table width="100%">
  <tr>
    <th align="center" width="33%"><h3>Project Root</h3></th>
    <th align="center" width="33%"><h3>Core Game Module</h3></th>
    <th align="center" width="33%"><h3>Test Suite</h3></th>
  </tr>
  <tr valign="top">
    <td>
      <pre>
rummikub/
├── rummikub/                   # Core Game Module
├── tests/                      # Test Suite
├── main.py                     # Project entry point
├── README.md                   # Project documentation
├── LICENSE                     # Project license
├── .gitignore                  # Git ignore configurations
├── pytest.ini                  # PyTest configuration
├── run_tests.py                # Test runner script
├── readme_images/              # Images for documentation
├── docs/                       # Documentation files
│   ├── rummikub_rules.pdf
│   └── project_description.odt
└── requirements/               # Dependency specifications
    ├── environment.yaml
    └── requirements.txt
      </pre>
    </td>
    <td>
      <pre>
rummikub/
├── assets/             # Game assets (images, sounds)
├── screens/            # Screen management modules              
│   ├── menu.py         # Menu systems and setup
│   └── game_screen.py  # Main gameplay screen
├── board.py            # Board state and validation
├── deck.py             # Tile creation and management
├── game.py             # Main game controller
├── message_system.py   # User feedback notifications
├── player.py           # Player state management
├── theme_manager.py    # UI styling and consistency
├── tile.py             # Tile objects and behaviors
└── utils.py            # Helper utilities
      </pre>
    </td>
    <td>
      <pre>
tests/
├── conftest.py                 # Shared test fixtures
├── unit/                       # Component unit tests
│   ├── test_board.py
│   ├── test_deck.py
│   ├── test_game.py
│   ├── test_message_system.py
│   ├── test_player.py
│   ├── test_theme_manager.py
│   ├── test_tile.py
│   └── test_utils.py
├── integration/                # Component interactions
│   ├── test_game_board.py
│   └── test_player_actions.py
└── functional/                 # End-to-end tests
    └── test_gameplay.py
      </pre>
    </td>
  </tr>
</table>

<br>

## Graph-Based Set Detection
The most technically complex aspect is the implementation of a graph-based algorithm for detecting valid Rummikub sets:
```python
class Graph:
    """
    Optimized adjacency matrix representation of the playing board,
    that works with an external dictionary of board tiles.
    """

    def __init__(self, max_size: int):
        self.size = max_size
        # Distance matrix: initialize with infinity, diagonal set to 0.
        self.matrix = np.full((self.size, self.size), np.inf)
        np.fill_diagonal(self.matrix, 0)
        # Vertex data: Each row holds [x, y, tile_id]. Uninitialized rows are [-1, -1, -1].
        self.vertex_data = np.full((self.size, 3), -1, dtype=int)
    
    def kruskals_msf(self, active_tiles: dict, max_weight: float):
        """
        Computes a minimum spanning forest with a max weight threshold.
        'active_tiles' is a dictionary {tile_id: Tile}.
        """

        active_ids = np.array(list(active_tiles.keys()), dtype=int)
        if active_ids.size == 0:
            return []
        
        submatrix = self.matrix[np.ix_(active_ids, active_ids)]
        triu_idx = np.triu_indices_from(submatrix, k=1)
        edges = np.column_stack((active_ids[triu_idx[0]], active_ids[triu_idx[1]]))
        weights = submatrix[triu_idx]
        
        valid = weights <= max_weight
        edges, weights = edges[valid], weights[valid]
        sorted_indices = np.argsort(weights)
        edges, weights = edges[sorted_indices], weights[sorted_indices]
        
        parent = np.arange(self.size)
        rank = np.zeros(self.size, dtype=int)
        
        def find(i):
            if parent[i] != i:
                parent[i] = find(parent[i])
            return parent[i]
        
        def union(x, y):
            root_x, root_y = find(x), find(y)
            if root_x != root_y:
                if rank[root_x] < rank[root_y]:
                    parent[root_x] = root_y
                elif rank[root_x] > rank[root_y]:
                    parent[root_y] = root_x
                else:
                    parent[root_y] = root_x
                    rank[root_x] += 1
        
        edge_used = []
        for u, v in edges:
            if find(u) != find(v):
                union(u, v)
                edge_used.append((u, v, self.matrix[u, v]))
        
        forest_map = {}
        for tid in active_ids:
            root = find(tid)
            if root not in forest_map:
                forest_map[root] = []
            forest_map[root].append(tid)
        
        forests = [(vertices, [(u, v, self.matrix[u, v])
                    for u, v, _ in edge_used if u in vertices or v in vertices])
                   for vertices in forest_map.values()]
        return forests
```
- Uses an **adjacency matrix** representation for spatial relationships between tiles
- Employs **Kruskal's minimum spanning forest algorithm** to identify connected tile sets
- Applies geometric distance calculations to determine tile proximity
- Optimizes tile operations with NumPy arrays for performance


## Menu System Implementation
The menu system (menu.py) provides a comprehensive user interface for game setup and transitions:

```python
class SetupMenu:
    """
    Initial game setup and home screen with comprehensive game information 
    and visual examples of gameplay elements.
    """

    def __init__(self, game, end_message=None):
        self.game = game
        self.current_page = "MAIN"  # Track which page we're viewing
        
        # Define a custom theme with the game's color scheme
        custom_theme = themes.THEME_DARK.copy()
        custom_theme.background_color = (0, 100, 50)  # Richer green background
        custom_theme.title_font_size = 60
        custom_theme.widget_font_size = 36
        custom_theme.widget_font_color = (255, 255, 255)
        
        # Create the main menu
        self.menu = pygame_menu.Menu(
            title="Rummikub",
            height=game.screen.get_height(),
            width=game.screen.get_width(),
            theme=custom_theme
        )
        
        # Store references to different "pages" (menus)
        self.menus = {
            "MAIN": self.menu,
            "RULES": self._create_rules_menu(),
            "EXAMPLES": self._create_examples_menu(),
            "SETUP": self._create_setup_menu()
        }
        
        # Initialize the main menu
        self._setup_main_menu(end_message)
        
        # Set initial menu based on context
        if end_message:
            self.current_page = "SETUP"
            self.menu = self.menus["SETUP"]
        
    def _create_rules_menu(self):
        """Create the rules page."""
        rules_menu = pygame_menu.Menu(
            title="Game Rules",
            height=self.game.screen.get_height(),
            width=self.game.screen.get_width(),
            theme=self.menu.get_theme()
        )
```
- **Multi-page design**: Separate pages for rules, examples, and player setup
- **Visual examples**: Demonstrates valid tile sets with visual examples
- **Dynamic content**: Adapts to game state (initial launch vs. end-of-game)
- **Integrated styling**: Uses custom themes from pygame_menu
- **Input validation**: Player name input with validation

## Rendering Pipeline
The rendering system employs a layered approach:
1. **Base layer**: Background colors and board areas
2. **Game elements**: Board tiles and player rack
3. **UI components**: Buttons and status information
4. **Overlay layer**: Messages and highlights

The ThemeManager provides centralized control over visual elements:

```python
@classmethod
def draw_button(cls, surface: pygame.Surface, rect: pygame.Rect, text: str, 
               color_name: str = 'button', text_color: str = 'button_text',
               hover: bool = False) -> None:
    """Draw a themed button on the given surface."""
    # Draw button background
    bg_color = cls.get_color('button_hover' if hover else color_name)
    pygame.draw.rect(surface, bg_color, rect, border_radius=10)
    
    # Draw button border
    border_color = cls.get_color('highlight' if hover else 'tile_border')
    pygame.draw.rect(surface, border_color, rect, width=2, border_radius=10)
    
    # Draw button text
    text_surf = cls.render_text(text, 'button', text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)
```
- **Consistent styling**: Unified color palette and font settings
- **Dynamic effects**: Hover states and animations
- **Responsive layout**: Adapts to screen dimensions
- **Visual feedback**: Color-coded messages and highlights

## Tile Manipulation System

Tiles implement a comprehensive interaction model:

```python
def start_drag(self, mouse_pos) -> None:
    self.dragging = True
    # Save tiles pre-drag position
    self.pre_drag_pos = self.get_coordinates()
    self.drag_offset = (self.rect.x - mouse_pos[0], self.rect.y - mouse_pos[1])

def update_drag(self, mouse_pos) -> None:
    if self.dragging:
        self.set_coordinates(
            mouse_pos[0] + self.drag_offset[0],
            mouse_pos[1] + self.drag_offset[1]
        )
```
- **Drag and drop**: Intuitive movement of tiles between rack and board
- **Position memory**: Tiles remember their starting position for move reversion
- **Collision detection**: Prevents overlapping tiles
- **Visual feedback**: Highlights valid and invalid placements
- **Snap alignment**: Automatically aligns tiles in valid sets

## Game Rules Enforcement

The code implements complete Rummikub rules:

```python
def validate_turn(self) -> bool:
    """Validate the current player's turn."""
    if len(self.game_screen.board.added_tiles) > 0:
        if self.check_initial_meld():
            if self.game_screen.board.validate_sets():
                return True
    else:
        print('No tiles played.')
    
    self.statistics['invalid_moves'] += 1
    return False
```
- **Initial meld**: 30-point minimum for first play
- **Set validation**: Checks for valid groups (same number, different colors)
- **Run validation**: Checks for valid runs (consecutive numbers, same color)
- **Joker handling**: Special rules for joker substitution
- **Board manipulation**: Allows rearranging existing tiles

## Message Notification System

The MessageSystem provides informative feedback:

```python
class MessageSystem:
    """Manages game messages and notifications."""
    
    def __init__(self):
        self.messages: List[Message] = []
        self.max_messages = 3
        self.vertical_spacing = 50
    
    def add_message(self, text: str, duration: float = 3.0, color_name: str = 'text',
                   font_name: str = 'normal', position: Tuple[int, int] = None) -> None:
        """Add a new message to the system."""
        self.messages.append(Message(text, duration, color_name, font_name, position))
        
        # Trim excess messages
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)
    
    def update(self) -> None:
        """Update all active messages, removing expired ones."""
        self.messages = [msg for msg in self.messages if msg.update()]
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw all active messages to the screen."""
        for i, message in enumerate(self.messages):
            y_pos = 100 + i * self.vertical_spacing
            message.draw(surface, default_y=y_pos)
    
    def clear(self) -> None:
        """Clear all messages."""
        self.messages.clear()
```
- **Temporal management**: Messages appear and disappear automatically
- **Fade effects**: Smooth transitions with alpha blending
- **Priority queue**: Multiple messages display in sequence
- **Visual styling**: Color-coded by message type (error, success, info)
- **Flexible positioning**: Default or custom message placement

## Statistical Tracking

The game maintains statistical information:

```python
# Add statistics tracking
self.statistics = {
    'turns_played': 0,
    'tiles_drawn': 0,
    'valid_sets_formed': 0,
    'invalid_moves': 0
}
```
- **Game progression**: Tracks turns played and player actions
- **Performance metrics**: Records valid sets and invalid moves
- **Deck status**: Monitors remaining tiles
- **End-game summary**: Provides statistics at game completion

## Audio Feedback System

The game includes sound effects for enhanced player experience:

```python
def load_sounds(self):
    """Load game sound effects."""
    self.sounds = {
        'tile_place': pygame.mixer.Sound('./rummikub/assets/sounds/tile_place.wav'),
        'invalid_move': pygame.mixer.Sound('./rummikub/assets/sounds/invalid_move.wav'),
        'draw_tile': pygame.mixer.Sound('./rummikub/assets/sounds/draw_tile.wav'),
        'valid_set': pygame.mixer.Sound('./rummikub/assets/sounds/valid_set.wav'),
        'win': pygame.mixer.Sound('./rummikub/assets/sounds/win.wav')
    }
```
- **Event-driven**: Sounds tied to specific game actions
- **Graceful degradation**: Falls back silently if sound system unavailable
- **Contextual feedback**: Different sounds for different game states


