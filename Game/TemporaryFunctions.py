def ai(totalMana, handSize, hand=[], currentSelection=[]):
    # Base case: If totalMana or handSize is 0, return the currentSelection
    if totalMana == 0 or handSize == 0:
        return currentSelection
    
    # If the last card in the hand has the same value as totalMana,
    # add it to the currentSelection and return the updated currentSelection
    if hand[handSize - 1] == totalMana:
        currentSelection.append(hand[handSize - 1])
        return currentSelection
        
    # If the last card in the hand is greater than totalMana,
    # recursively call the ai function with handSize - 1
    elif hand[handSize - 1] > totalMana:
        return ai(totalMana, handSize - 1, hand, currentSelection)
    
    # If the last card in the hand is less than totalMana,
    # add it to the currentSelection and recursively call the ai function
    # with totalMana - hand[handSize - 1] and handSize - 1
    else:
        currentSelection.append(hand[handSize - 1])
        return ai(totalMana - hand[handSize - 1], handSize - 1, hand, currentSelection)
        
hand = [1, 2, 3, 4, 5]
totalMana = 7
handSize = len(hand)
playedHand = list()

# Call the ai function with the given parameters
ai(totalMana, handSize, hand, playedHand)

print(playedHand)



def draw_card(screen, card, x, y, small_form=True):
    # Card dimensions
    small_card_width, small_card_height = 100, 150
    large_card_width, large_card_height = 200, 300
    border_color = (255, 255, 255)  # White border
    text_color = (255, 255, 255)    # White text

    card_rect = pygame.Rect(x, y, small_card_width, small_card_height)
    if card_rect.collidepoint(pygame.mouse.get_pos()):
        small_form = False

    if small_form:
        # Create a rectangle for the small card
        card_rect = pygame.Rect(x, y, small_card_width, small_card_height)
        pygame.draw.rect(screen, border_color, card_rect, 2)  # 2 pixels for the border thickness

        # Font setup
        font = pygame.font.Font(None, 12)

        # Name (centered at the top)
        name_surf = font.render(card.name, True, text_color)
        name_rect = name_surf.get_rect(center=(x + small_card_width // 2, y + 15))
        screen.blit(name_surf, name_rect)

        # Tier (top right)
        tier_surf = font.render(f"Tier: {card.tier}", True, text_color)
        tier_rect = tier_surf.get_rect(topright=(x + small_card_width - 5, y + 5))
        screen.blit(tier_surf, tier_rect)

        # Image (placeholder for now)
        pygame.draw.rect(screen, (180, 180, 180), (x + 10, y + 30, small_card_width - 20, 60))  # Grey rectangle as placeholder

        # Health (bottom left)
        hp_surf = font.render(f"HP: {card.hp}", True, text_color)
        hp_rect = hp_surf.get_rect(bottomleft=(x + 5, y + small_card_height - 5))
        screen.blit(hp_surf, hp_rect)

        # Attack (bottom right)
        attack_surf = font.render(f"Attack: {card.attack}", True, text_color)
        attack_rect = attack_surf.get_rect(bottomright=(x + small_card_width - 5, y + small_card_height - 5))
        screen.blit(attack_surf, attack_rect)

        pygame.display.flip()
    else:
        # Create a rectangle for the large card
        card_rect = pygame.Rect(x, y, large_card_width, large_card_height)
        pygame.draw.rect(screen, border_color, card_rect, 2)  # 2 pixels for the border thickness

        # Font setup
        font = pygame.font.Font(None, 18)

        # Name (centered at the top)
        name_surf = font.render(card.name, True, text_color)
        name_rect = name_surf.get_rect(center=(x + large_card_width // 2, y + 20))
        screen.blit(name_surf, name_rect)

        # Image (placeholder for now)
        pygame.draw.rect(screen, (180, 180, 180), (x + 20, y + 40, large_card_width - 40, 120))  # Grey rectangle as placeholder

        # Description (below the image)
        desc_surf = font.render(card.description, True, text_color)
        desc_rect = desc_surf.get_rect(center=(x + large_card_width // 2, y + 200))
        screen.blit(desc_surf, desc_rect)

        # Tier (top right)
        tier_surf = font.render(f"Tier: {card.tier}", True, text_color)
        tier_rect = tier_surf.get_rect(topright=(x + large_card_width - 10, y + 10))
        screen.blit(tier_surf, tier_rect)

        # Health (bottom left)
        hp_surf = font.render(f"HP: {card.hp}", True, text_color)
        hp_rect = hp_surf.get_rect(bottomleft=(x + 10, y + large_card_height - 10))
        screen.blit(hp_surf, hp_rect)

        # Attack (bottom right)
        attack_surf = font.render(f"Attack: {card.attack}", True, text_color)
        attack_rect = attack_surf.get_rect(bottomright=(x + large_card_width - 10, y + large_card_height - 10))
        screen.blit(attack_surf, attack_rect)

        pygame.display.flip()

def draw_deck():
    screen.fill((0, 140, 60))  # Clear the screen
    card_x, card_y = 50, 50  # Start position for the first card
    for card in game_manager.player_deck.cards: # type: ignore (suppress warnings from IDE)
        small_form = True
        card_rect = pygame.Rect(card_x, card_y, 100, 150)
        if card_rect.collidepoint(pygame.mouse.get_pos()):
            small_form = False
        draw_card(screen, card, card_x, card_y, small_form)
        card_x += 120  # Move to the right for the next card
        if card_x + 100 > 800:  # Check if we need to wrap to the next row
            card_x = 50
            card_y += 170

    pygame.display.flip()  # Update the display once after initial draw

# Draw the initial deck
draw_deck()
pygame.display.flip()  # Update the display once after initial draw