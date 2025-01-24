# Rummikub

## Introduction
Welcome to my Rummikub project! This repository contains the Python implementation of the popular tile-based game, Rummikub. In this project, I am building the game from scratch, following the traditional rules and mechanics of Rummikub. The README provides an overview of the game, including the official rules and explanations of core gameplay elements.

The rules and functionalities of the game are listed below, with checkboxes next to each item. These checkboxes help track the progress of the implementation, allowing you to see which features are completed and which are still in progress. As the development continues, this README will serve as both a guide to the game’s rules and a progress tracker for the ongoing work in the project.

## Game Rules
### Objective
The goal of Rummikub is to be the first player to eliminate all tiles from your rack by forming valid sets (groups or runs) on the table. The game ends when a player empties their rack or when no more moves can be made.

### Game Setup
- [x] 1. Players: 2–4 players. 
- [x] 2. Tiles: 106 tiles numbered 1 to 13 in four colors: red, blue, orange, and black. There are two identical tiles for each number and color. There are also two jokers.
- [x] 3. Rack: Each player uses a rack to hold their tiles.
- [x] 4. Tile Distribution:
    - [x] Shuffle all tiles in deck.
    - [x] Each player draws 14 tiles and places them on their rack.
    - [x] The remaining tiles form a pool in the center, known as the draw pile.

### Gameplay
- [ ] 1. Starting the Game 
    - [x] Players determine the starting player drawing tiles.
    - [x] Play proceeds clockwise.
- [x] 2. Initial Meld:
    - [x] Each player must make an initial meld to enter the game.
    - [x] The initial meld must use tiles from the player’s rack and have a total value of at least 30 points.
    - [x] Tiles used for the initial meld must form valid sets (explained below).
    - [x] If a player cannot make an initial meld, they must draw a tile from the draw pile and pass their turn.
- [ ] 3. Turns: 
    - [ ] On their turn, a player can:
        - [x] Play tiles from their rack to create or extend sets on the table.
        - [ ] Manipulate existing sets on the table to create new sets, provided all tiles remain part of valid sets after the manipulation.
    - [x] If no moves are possible or the player chooses not to play, they must draw a tile and pass their turn.
- [x] 4. Ending a Turn:
    - [x] A player’s turn ends when they have successfully played tiles and all sets on the table are valid.
    - [x] If a player draws a tile, they cannot play it immediately and must wait until their next turn.

### Valid Sets
There are two types of valid sets:
- [x] 1. Groups:
    - [x] A group consists of 3 or 4 tiles of the same number but different colors.
    - Example: `{7 (red), 7 (blue), 7 (orange)}`.
- [x] 2. Runs:
    - [x] A run consists of 3 or more consecutive numbers in the same color.
    - Example: `{5 (blue), 6 (blue), 7 (blue)}`.

### Jokers
- [x] The two jokers can substitute for any tile in a set.
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
    - Example: `{7 (red), 7 (blue), 7 (orange)} and {5 (orange), 6 (orange), 7 (orange)} can be rearranged as {5 (orange), 6 (orange), 7 (orange), 7 (blue)} and {7 (red), 7 (orange)}`.
- [ ] 2. Joker Penalty
    - [ ] A joker left on a player’s rack at the end of the game incurs a penalty of 30 points.
- [ ] 3. Time Limit
    - [ ] Players may agree to a time limit for turns to keep the game moving.


## Project File Structure:
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

