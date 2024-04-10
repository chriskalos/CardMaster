import random
from Card import cards_list

deck_size = 25 # todo: Deck size should be 5 times the number of matches so far

class Deck:
    def __init__(self):
        self.cards = []  # Start with an empty list of cards

    def shuffle(self):
        """Shuffle the deck of cards."""
        random.shuffle(self.cards)

    def draw(self):
        """Draw a card from the deck, removing it from the deck."""
        if not self.cards:
            raise ValueError("No cards left in the deck!")
        return self.cards.pop()

    def generate_deck(self):
        """Generate a deck of 25 cards randomly picked from the available card list."""
        self.cards = random.choices(cards_list, k=deck_size)
        self.shuffle()  # Optional: Shuffle the deck after generation

# Example usage
deck = Deck()
deck.generate_deck()
print(f"Deck has {len(deck.cards)} cards.")
for i in range(5):  # Draw some cards to see what we got
    print(deck.draw().get_card_info())
