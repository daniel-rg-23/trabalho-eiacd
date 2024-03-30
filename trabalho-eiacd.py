#interface da matriz
import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants for the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOR = (0,147,175)  # Background color as an RGB tuple
GRID_SIZE = 4
TILE_SIZE = 100
TILE_MARGIN = 20

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Match the Tiles")

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game logic would go here

    # Clear the screen
    screen.fill(BG_COLOR)

    # Draw the game board
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            tile_x = col * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN
            tile_y = row * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN
            pygame.draw.rect(screen, (255, 255, 255), 
                             (tile_x, tile_y, TILE_SIZE, TILE_SIZE))

    # Update the display
    pygame.display.flip()

# Exit Pygame
pygame.quit()
sys.exit()

