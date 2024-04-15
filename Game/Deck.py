import random
from Card import cards_list

class Deck:
    def __init__(self):
        self.cards = []  # Start with an empty list of cards

    def shuffle(self):
        """Shuffle the deck of cards."""
        random.shuffle(self.cards)

    def randomiser(self, lowest_tier: int, highest_tier: int):
        # print(f"### - Lowest tier: {lowest_tier}, Highest tier: {highest_tier}")
        if lowest_tier < 1:
            lowest_tier = 1
        if highest_tier < 1:
            highest_tier = 1
        if random.random() < 0.05 and highest_tier > 3:
            chosen_card = random.choice([card for card in cards_list if card.tier <= highest_tier and card.card_class.name == "RARE"])
        else:
            chosen_card = random.choice([card for card in cards_list if card.tier >= lowest_tier and card.tier <= highest_tier and card.card_class.name != "RARE"])
        return chosen_card

    def draw(self):
        """Draw a card from the deck, removing it from the deck."""
        if not self.cards:
            raise ValueError("No cards left in the deck!")
        return self.cards.pop()
    
    def __str__(self):
        """Return a string of the current deck information."""
        deck_info = ""
        i = 0
        for card in self.cards:
            deck_info += f"Card {i}:\n{card.get_card_info()}"
            i += 1
        return deck_info