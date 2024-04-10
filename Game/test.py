import pygame
import sys

# Initialize PyGame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))

# Set the title of the window
pygame.display.set_caption('CardMaster Test')

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color
    screen.fill((0, 140, 60))

    # Update the display
    pygame.display.flip()

# Quit PyGame
pygame.quit()
sys.exit()
