import pygame
from GameManager import GameManager

# Initialize PyGame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((1024, 768))
pygame.display.set_caption('Card Game')

# Initialize font
pygame.font.init()
font = pygame.font.Font(None, 24)

# Create an instance of GameManager
game_manager = GameManager()
game_manager.instantiate_player_deck()  # Create the initial deck

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Additional event handling can go here

    # Clear the screen
    screen.fill((0, 140, 60))

    # Display cards in the deck
    y_offset = 20  # Starting y position to display cards
    for card in game_manager.player_deck.cards:
        card_text = font.render(f"{card.name} - {card.description} | HP: {card.hp}, Attack: {card.attack}, Tier: {card.tier}, Class: {card.card_class.name}, Effect: {card.effect_description}", True, (255, 255, 255))
        screen.blit(card_text, (50, y_offset))
        y_offset += 30  # Increment y position for the next card

    # Update the display
    pygame.display.flip()

# Quit PyGame
pygame.quit()
