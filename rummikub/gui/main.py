import pygame

# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((2400, 1800))

# Title and Icon
pygame.display.set_caption("Rummikub")
icon = pygame.image.load('./icons/pngegg.png')
pygame.display.set_icon(icon)

# List to track sets of tiles
sets = []
tiles = []
num_tiles = 3

# Tile class to represent each tile
class Tile:
    def __init__(self, image, num, x, y):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.num = num
        self.rect.x = x
        self.rect.y = y
        self.current_set = None  # This will track which set the tile belongs to
    
    def __repr__(self):
        return f'{self.num}'

    def draw_tile(self):
        screen.blit(self.image, self.rect)

# Create initial tile instances
x = 0
for i in range(num_tiles):
    tiles.append(Tile(f'./tiles/tile_{i+1}_red.png',i+1, x, 900))
    x += 200  # Move each tile by 200 pixels

# Function to check if two tiles are close enough to form a set
def check_proximity(tile1, tile2, threshold=170):
    return abs(tile1.rect.x - tile2.rect.x) < threshold

# Function to check if a dragged tile collides with any other tile
def check_overlap(dragged_tile, threshold=140):
    for other_tile in tiles:
        if other_tile != dragged_tile:
            if dragged_tile.rect.colliderect(other_tile.rect):
                return True
    return False

# Function to group tiles together into sets
def update_sets():
    global sets

    # For each tile, if it's not in any set, place it in its own set
    for tile in tiles:
        if tile.current_set is None:
            new_set = [tile]
            tile.current_set = new_set
            sets.append(new_set)

    # Merge sets that are close enough to each other
    for tile in tiles:
        for other_tile in tiles:
            if tile != other_tile and check_proximity(tile, other_tile):
                # If the two tiles are close enough, merge their sets
                if tile.current_set != other_tile.current_set:
                    # Remove the old sets before merging
                    old_set = other_tile.current_set
                    if old_set in sets:
                        sets.remove(old_set)
                    
                    # Merge the sets
                    new_set = tile.current_set + old_set
                    tile.current_set = new_set
                    for t in new_set:
                        t.current_set = new_set
                    sets.append(new_set)

    # Now, remove any individual sets that have been merged
    sets = [s for s in sets if len(s) > 1]  # Remove any sets that only have one tile

    # Check for tiles that are too far away from their current set and remove them
    for current_set in sets:
        for tile in current_set:
            # Check if this tile is too far away from the rest of the set
            if all(check_proximity(tile, other_tile, threshold=200) == False for other_tile in current_set):
                current_set.remove(tile)
                tile.current_set = None

# Function to draw all tiles and print active sets
def draw_tiles():
    for tile in tiles:
        tile.draw_tile()
    

# Game loop
running = True
dragging = False
offset_x, offset_y = 0, 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle mouse button down (start dragging)
        if event.type == pygame.MOUSEBUTTONDOWN:
            for tile in tiles:
                if tile.rect.collidepoint(event.pos):
                    dragging = True
                    offset_x = tile.rect.x - event.pos[0]
                    offset_y = tile.rect.y - event.pos[1]

        # Handle mouse button up (stop dragging)
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
            update_sets()  # After placing the tile, check and update the sets
            print(f'Active Sets: {sets}')  # Print the active sets

        # Handle mouse motion (dragging tiles)
        if dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for tile in tiles:
                if tile.rect.collidepoint(event.pos):
                    # Move the dragged tile
                    tile.rect.x = mouse_x + offset_x
                    tile.rect.y = mouse_y + offset_y

                    # Check for overlap and adjust if necessary (only for the dragged tile)
                    if check_overlap(tile):
                        # Revert to the previous position if overlapping
                        tile.rect.x = offset_x
                        tile.rect.y = offset_y
                    else:
                        # Boundary checks for tile movement
                        if tile.rect.x <= 0:
                            tile.rect.x = 0
                        elif tile.rect.x >= 2260:
                            tile.rect.x = 2260

                        if tile.rect.y <= 0:
                            tile.rect.y = 0
                        elif tile.rect.y >= 1560:
                            tile.rect.y = 1560

    # Draw Background
    screen.fill((0, 128, 0))  # Green background

    # Draw all tiles
    draw_tiles()

    # Update display
    pygame.display.update()

pygame.quit()

