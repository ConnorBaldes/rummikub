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

# # Function to group tiles together into sets
# def update_sets(sets, moved_tile):

#     # TO DO: When going from 3 in a set down to 1 then back to 3, only the 'moved_tile' and first valid occurance of 'other_tile'
#     #        are added to the new set. Need to change the creating of the new set, to check for tiles next to 'other_tile' or another
#     #        tile next to 'moved_tile'

#     for other_tile in tiles:
#         if moved_tile != other_tile and abs(moved_tile.rect.x - other_tile.rect.x) < 170 and abs(moved_tile.rect.y - other_tile.rect.y) < 120:

#             if moved_tile.current_set != other_tile.current_set or (moved_tile.current_set == None and other_tile.current_set == None):

#                 if moved_tile.current_set != None:
#                     if moved_tile.current_set in sets:
#                         sets.remove(moved_tile.current_set)
#                     moved_tile.current_set = None
#                 if other_tile.current_set != None:

#                     print(f'Current Set: {other_tile.current_set}')
#                     (other_tile.current_set).append(moved_tile)
#                     print(f'Current Set: {other_tile.current_set}')
#                     moved_tile.current_set = other_tile.current_set
#                 else:

#                     new_set = []
#                     new_set.append(moved_tile)
#                     new_set.append(other_tile)
#                     sets.append(new_set)
#                     moved_tile.current_set = new_set
#                     other_tile.current_set = new_set
                    

#     # Remove tiles that are too far from their set
#     for current_set in sets:
#         for tile in current_set:
#             close = False      
#             for other_tile in current_set:
#                 if  tile != other_tile and abs(tile.rect.x - other_tile.rect.x) < 220 and abs(tile.rect.y - other_tile.rect.y) < 180:
#                     close = True
#             if not close:
#                 current_set.remove(tile)
#                 tile.current_set = None

#     # Remove single-tile sets
#     for curent_set in sets:
#         if len(current_set) < 2:
#             current_set[0].current_set = None
#             sets.remove(current_set)
            
                



# # Function to draw all tiles
# def draw_tiles():
#     for tile in tiles:
#         tile.draw_tile()"





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
                    board.distance_matrix.print_matrix()
                    board.update_distances()
                    board.get_forests()
                    #board.update_sets()  # Update sets after placement
                    #board.print_active_sets()

            dragging = None

        # Handle mouse motion (dragging tiles)
        elif event.type == pygame.MOUSEMOTION and dragging:
            dragging.rect.x = event.pos[0] + offset_x
            dragging.rect.y = event.pos[1] + offset_y

            # Prevent movement outside the board
            dragging.rect.x = max(0, min(2260, dragging.rect.x))
            dragging.rect.y = max(0, min(1560, dragging.rect.y))

    # Draw Background
    board.screen.fill((0, 128, 0))  # Green background

    # Draw all tiles
    board.draw_tiles()

    # Update display
    pygame.display.update()

pygame.quit()
