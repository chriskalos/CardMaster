def draw_deck(screen, deck, x, y):
    card_spacing = 120
    card_width = 100
    deck_width = len(deck.cards) * card_spacing
    x_start = x - deck_width // 2
    for i, card in enumerate(deck.cards):
        draw_card(screen, card, x_start + i * card_spacing, y)