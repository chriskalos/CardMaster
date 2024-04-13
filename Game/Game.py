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

def draw_card(screen, card, x, y):
    # Card dimensions
    card_width, card_height = 100, 150
    border_color = (255, 255, 255)  # White border
    text_color = (255, 255, 255)    # White text

    # Create a rectangle for the card
    card_rect = pygame.Rect(x, y, card_width, card_height)
    pygame.draw.rect(screen, border_color, card_rect, 2)  # 2 pixels for the border thickness

    # Font setup
    font = pygame.font.Font(None, 20)

    # Name (centered at the top)
    name_surf = font.render(card.name, True, text_color)
    name_rect = name_surf.get_rect(center=(x + card_width // 2, y + 15))
    screen.blit(name_surf, name_rect)

    # Image (placeholder for now)
    pygame.draw.rect(screen, (180, 180, 180), (x + 10, y + 30, card_width - 20, 60))  # Grey rectangle as placeholder

    # Description (below the image)
    desc_surf = font.render(card.description, True, text_color)
    desc_rect = desc_surf.get_rect(center=(x + card_width // 2, y + 100))
    screen.blit(desc_surf, desc_rect)

    # Tier (top right)
    tier_surf = font.render(f"Tier: {card.tier}", True, text_color)
    tier_rect = tier_surf.get_rect(topright=(x + card_width - 5, y + 5))
    screen.blit(tier_surf, tier_rect)

    # Health (bottom left)
    hp_surf = font.render(f"HP: {card.hp}", True, text_color)
    hp_rect = hp_surf.get_rect(bottomleft=(x + 5, y + card_height - 5))
    screen.blit(hp_surf, hp_rect)

    # Attack (bottom right)
    attack_surf = font.render(f"Attack: {card.attack}", True, text_color)
    attack_rect = attack_surf.get_rect(bottomright=(x + card_width - 5, y + card_height - 5))
    screen.blit(attack_surf, attack_rect)

# Helper to draw the deck
def draw_deck():
    screen.fill((0, 140, 60))  # Clear the screen
    card_x, card_y = 50, 50  # Start position for the first card
    for card in game_manager.player_deck.cards: # type: ignore (suppress warnings from IDE)
        draw_card(screen, card, card_x, card_y)
        card_x += 110  # Move to the right for the next card
        if card_x + 100 > 800:  # Check if we need to wrap to the next row
            card_x = 50
            card_y += 160

# Draw the initial deck
draw_deck()
pygame.display.flip()  # Update the display once after initial draw

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Here, add any event that requires re-drawing the deck
        # For example, adding or removing a card, shuffling the deck, etc.
        # You would call `draw_deck()` followed by `pygame.display.flip()` in response to such events.

# Quit PyGame
pygame.quit()
