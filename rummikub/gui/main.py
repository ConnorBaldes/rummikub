import pygame
from board import Board
# Initialize pygame
pygame.init()

board = Board()

# Function to check if a dragged tile collides with any other tile
def check_overlap(dragged_tile):
    for other_tile in board.get_tile_positions():
        if board.deck.tiles[other_tile].id != dragged_tile.id and dragged_tile.rect.colliderect(board.deck.tiles[other_tile].rect):
            return True  # Collision detected
    return False

# Game loop
running = True
dragging = None  # Track the tile being dragged
offset_x, offset_y = 0, 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle mouse button down (start dragging)
        if event.type == pygame.MOUSEBUTTONDOWN:
            for tile in board.deck.tiles:
                if board.deck.tiles[tile].rect.collidepoint(event.pos):
                    dragging = board.deck.tiles[tile]
                    offset_x = board.deck.tiles[tile].rect.x - event.pos[0]
                    offset_y = board.deck.tiles[tile].rect.y - event.pos[1]
                    board.deck.tiles[tile].original_pos = (board.deck.tiles[tile].rect.x, board.deck.tiles[tile].rect.y)  # Store initial position

        # Handle mouse button up (stop dragging)
        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging:
                if check_overlap(dragging):  
                    dragging.rect.x, dragging.rect.y = dragging.original_pos  # Reset to original position if overlapping
                else:
                    board.distance_matrix.recompute_distances()
                    board.update_distances()
                    forests = board.get_forests()
                    #board.update_sets()  # Update sets after placement
                    # board.print_active_sets()
                    board.tile_graph.print_forests(forests)

            dragging = None

        # Handle mouse motion (dragging tiles)
        elif event.type == pygame.MOUSEMOTION and dragging:
            dragging.rect.x = event.pos[0] + offset_x
            dragging.rect.y = event.pos[1] + offset_y

            # Prevent movement outside the board
            dragging.rect.x = max(0, min(2860, dragging.rect.x))
            dragging.rect.y = max(0, min(1860, dragging.rect.y))

    # Draw Background
    board.screen.fill((0, 128, 0))  # Green background

    # Draw all tiles
    board.draw_tiles()

    # Update display
    pygame.display.update()

pygame.quit()
