# Rummikub

## Game Rules

### Objective
The goal of Rummikub is to be the first player to eliminate all tiles from your rack by forming valid sets (groups or runs) on the table. The game ends when a player empties their rack or when no more moves can be made.

### Game Setup
- [ ] 1. Players: 2–4 players. 
- [ ] 2. Tiles: 106 tiles numbered 1 to 13 in four colors: red, blue, yellow, and black. There are two identical tiles for each number and color. There are also two jokers.
- [ ] 3. Rack: Each player uses a rack to hold their tiles.
- [ ] 4. Tile Distribution:
    - [ ] Shuffle all tiles face down on the table.
    - [ ] Each player draws 14 tiles and places them on their rack.
    - [ ] The remaining tiles form a pool in the center, known as the draw pile.

### Gameplay
- [ ] 1. Starting the Game 
    - [ ] Players determine the starting player (e.g., by rolling dice or drawing tiles).
    - [ ] Play proceeds clockwise.
- [ ] 2. Initial Meld:
    - [ ] Each player must make an initial meld to enter the game.
    - [ ] The initial meld must use tiles from the player’s rack and have a total value of at least 30 points.
    - [ ] Tiles used for the initial meld must form valid sets (explained below).
    - [ ] If a player cannot make an initial meld, they must draw a tile from the draw pile and pass their turn.
- [ ] 3. Turns: 
    - [ ] On their turn, a player can:
        - [ ] Play tiles from their rack to create or extend sets on the table.
        - [ ] Manipulate existing sets on the table to create new sets, provided all tiles remain part of valid sets after the manipulation.
    - [ ] If no moves are possible or the player chooses not to play, they must draw a tile and pass their turn.
- [ ] 4. Ending a Turn:
    - [ ] A player’s turn ends when they have successfully played tiles and all sets on the table are valid.
    - [ ] If a player draws a tile, they cannot play it immediately and must wait until their next turn.

### Valid Sets
There are two types of valid sets:
- [ ] 1. Groups:
    - [ ] A group consists of 3 or 4 tiles of the same number but different colors.
    - [ ] Example: `{7 (red), 7 (blue), 7 (yellow)}`.
- [ ] 2. Runs:
    - [ ] A run consists of 3 or more consecutive numbers in the same color.
    - [ ] Example: `{5 (blue), 6 (blue), 7 (blue)}`.

### Jokers
- [ ] The two jokers can substitute for any tile in a set.
- [ ] Points for a joker match the tile it represents.
- [ ] A joker already on the table can be replaced by the tile it represents. The replacing tile must come from the player’s rack, not the draw pile.
- [ ] When a joker is replaced, it must be used as part of a new set in the same turn.

### Scoring
- [ ] 1. Winning the Game:
    - [ ] A player wins when they play their last tile.
    - [ ] All other players score penalty points equal to the sum of the tiles left on their racks.
    - [ ] The winner’s score is the sum of the penalty points from other players.
- [ ] 2. Ending Without a Winner:
    - [ ] If no players can make a move and the draw pile is empty, the game ends.
    - [ ] Players calculate their total tile values, and the player with the lowest score wins.

### Special Rules
- [ ] 1. Manipulating Sets
    - [ ] Players can rearrange tiles already on the table to form new sets, provided all sets remain valid at the end of the turn.
    - Example: `{7 (red), 7 (blue), 7 (yellow)} and {5 (yellow), 6 (yellow), 7 (yellow)} can be rearranged as {5 (yellow), 6 (yellow), 7 (yellow), 7 (blue)} and {7 (red), 7 (yellow)}`.
- [ ] 2. Joker Penalty
    - [ ] A joker left on a player’s rack at the end of the game incurs a penalty of 30 points.
- [ ] 3. Time Limit
    - [ ] Players may agree to a time limit for turns to keep the game moving.


### Project File Structure:
```
rummikub/
├── main.py              # Entry point for the game
├── README.md            # Documentation (overview, how to play, etc.)
├── requirements.txt     # Dependencies (if any)
├── rummikub/
│   ├── __init__.py      # Marks this directory as a package
│   ├── game.py          # Game coordination logic
│   ├── board.py         # Board-related classes and functions
│   ├── deck.py          # Deck-related classes and functions
│   ├── tile.py          # Tile class
│   ├── player.py        # Player-related classes
│   ├── utils.py         # Helper functions
│   ├── display.py       # Game-display related classes and functions
│   └── patterns/        # Design patterns
│       ├── __init__.py  
│       ├── observer.py  # Observer pattern implementation
│       └── state.py     # State pattern implementation
├── tests/               # Unit tests
│   ├── test_game.py     # Tests for game logic
│   ├── test_board.py    # Tests for the board
│   ├── test_deck.py     # Tests for the deck
│   ├── test_tile.py     # Tests for the tiles
│   └── test_player.py   # Tests for players
```

## Installation

## Usage

