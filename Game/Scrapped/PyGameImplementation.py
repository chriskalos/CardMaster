import pygame
from GameManager import GameManager  # Assuming GameManager and Card classes are defined in this module

# Initialize PyGame
pygame.init()

# Set up the display
window_width = 1920
window_height = 1080
screen = pygame.display.set_mode((window_width, window_height))
fps = 60
pygame.display.set_caption('Card Game')

# Initialize font
pygame.font.init()
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)


# Create an instance of GameManager
game_manager = GameManager()
game_manager.start_match()

def interpolate(value, target, speed):
    return value + (target - value) * speed  # Adjust speed to control animation duration

# Function to draw a card
def draw_card(screen, card, x, y, animation_states, index):
    state = animation_states[index]  # Retrieve the state using index
    card_frame_color = (255, 255, 255)
    card_background_color = (210, 210, 210) if state['small'] else (180, 180, 180)
    card_text_color = (255, 255, 255)
    card_tier_color = (0, 0, 255)
    card_hp_color = (255, 0, 0)
    card_attack_color = (0, 255, 0)
    card_width = state['width']
    card_height = state['height']

    # Mouse hover check
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if pygame.Rect(x - card_width // 2, y - card_height // 2, card_width, card_height).collidepoint((mouse_x, mouse_y)):
        if state['small']:
            state['small'] = False
            state['target_width'] = 200
            state['target_height'] = 300
    else:
        if not state['small']:
            state['small'] = True
            state['target_width'] = 100
            state['target_height'] = 150

    # Interpolate width and height
    state['width'] = interpolate(card_width, state['target_width'], 0.1)
    state['height'] = interpolate(card_height, state['target_height'], 0.1)

    # Draw the card based on current width and height...
    card_rect = pygame.Rect(x - card_width // 2, y - card_height // 2, card_width, card_height)
    pygame.draw.rect(screen, card_frame_color, card_rect, 2)
    pygame.draw.rect(screen, card_background_color, card_rect)

    # Card details drawing logic should use 'state['small']' and not 'animation_states[card]['small']'
    if state['small']:
        # Tier (top right)
        tier_surf = font.render(f"{card.tier}", True, card_tier_color)
        tier_rect = tier_surf.get_rect(topright=(x + card_width // 2 - 5, y - card_height // 2 + 5))
        screen.blit(tier_surf, tier_rect)

        # Health (bottom left)
        hp_surf = font.render(f"{card.hp}", True, card_hp_color)
        hp_rect = hp_surf.get_rect(bottomleft=(x - card_width // 2 + 5, y + card_height // 2 - 5))
        screen.blit(hp_surf, hp_rect)

        # Attack (bottom right)
        attack_surf = font.render(f"{card.attack}", True, card_attack_color)
        attack_rect = attack_surf.get_rect(bottomright=(x + card_width // 2 - 5, y + card_height // 2 - 5))
        screen.blit(attack_surf, attack_rect)

        # Name (centered at the top)
        name_surf = font.render(card.name, True, card_text_color)
        name_rect = name_surf.get_rect(center=(x, y - card_height // 2 + 15))
        screen.blit(name_surf, name_rect)
    else:
        card_font_size = 16

        # Create a rectangle for the card
        card_rect = pygame.Rect(x - card_width // 2, y - card_height // 2, card_width, card_height)
        pygame.draw.rect(screen, card_frame_color, card_rect, 2)  # 2 pixels for the border thickness

        # Background color
        card_background_color = (180, 180, 180)
        pygame.draw.rect(screen, card_background_color, (x - card_width // 2 + 2, y - card_height // 2 + 2, card_width - 4, card_height - 4))

        # Name (centered at the top)
        name_font = pygame.font.Font(None, card_font_size)
        name_lines = []
        words = card.name.split()
        current_line = ""
        for word in words:
            if name_font.size(current_line + " " + word)[0] <= card_width - 20:
                current_line += " " + word
            else:
                name_lines.append(current_line.strip())
                current_line = word
        name_lines.append(current_line.strip())

        for i, line in enumerate(name_lines):
            name_surf = font.render(line, True, card_text_color)
            name_rect = name_surf.get_rect(center=(x, y - card_height // 2 + 15 + i * card_font_size))
            screen.blit(name_surf, name_rect)

        # Image (placeholder for now)
        pygame.draw.rect(screen, (180, 180, 180), (x - card_width // 2 + 10, y - card_height // 2 + 30, card_width - 20, 60))  # Grey rectangle as placeholder

        # Description (below the image)
        desc_font = pygame.font.Font(None, card_font_size)
        desc_lines = []
        # Ensure there are two newlines between description and effect description.
        desc_and_effect = f"{card.description}\n\nEffect: {card.effect_description}"

        # Split the text into lines manually, respecting newlines
        # This splits on explicit newlines to create a list of lines, and then further splits each line into words.
        lines = desc_and_effect.split('\n')
        for line in lines:
            words = line.split()
            current_line = ""
            for word in words:
                # Check if adding the next word would exceed the width limit
                if desc_font.size(current_line + " " + word)[0] > card_width - 100:
                    desc_lines.append(current_line.strip())
                    current_line = word
                else:
                    current_line += " " + word
            # Append the last processed line if it contains text
            if current_line:
                desc_lines.append(current_line.strip())
            # Since we're processing explicit lines, add an empty string for each newline encountered
            desc_lines.append("")

        # Render each line
        for i, line in enumerate(desc_lines):
            if line:  # This check avoids attempting to render empty strings
                desc_surf = font.render(line, True, card_text_color)
                desc_rect = desc_surf.get_rect(center=(x, y - card_height // 2 + 100 + i * card_font_size))
                screen.blit(desc_surf, desc_rect)

        # Tier (top right)
        tier_surf = font.render(f"Tier: {card.tier}", True, card_tier_color)
        tier_rect = tier_surf.get_rect(topright=(x + card_width // 2 - 5, y - card_height // 2 + 5))
        screen.blit(tier_surf, tier_rect)

        # Health (bottom left)
        hp_surf = font.render(f"Health: {card.hp}", True, card_hp_color)
        hp_rect = hp_surf.get_rect(bottomleft=(x - card_width // 2 + 5, y + card_height // 2 - 5))
        screen.blit(hp_surf, hp_rect)

        # Attack (bottom right)
        attack_surf = font.render(f"Attack: {card.attack}", True, card_attack_color)
        attack_rect = attack_surf.get_rect(bottomright=(x + card_width // 2 - 5, y + card_height // 2 - 5))
        screen.blit(attack_surf, attack_rect)


# Initialize animation states for each card
animation_states = {}
for i, card in enumerate(game_manager.player.alive_deck.cards + game_manager.current_match.enemy.alive_deck.cards):
    animation_states[i] = {'width': 100, 'height': 150, 'target_width': 100, 'target_height': 150, 'small': True}

def draw_deck(screen, deck, x, y, start_index=0):
    card_spacing = 120
    for i, card in enumerate(deck.cards):
        index = start_index + i
        draw_card(screen, card, x + i * card_spacing, y, animation_states, index)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((59, 178, 115))  # Background color
    draw_deck(screen, game_manager.player.alive_deck, window_width // 8, window_height * 3 // 4 - 75, 0)
    draw_deck(screen, game_manager.current_match.enemy.alive_deck, window_width // 8, window_height // 4 + 75, len(game_manager.player.alive_deck.cards))
    clock.tick(fps)
    pygame.display.update()

# Quit PyGame
pygame.quit()