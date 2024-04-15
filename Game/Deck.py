import random
from Card import cards_list

deck_size = 10 # todo: Deck size should be 5 times the number of matches so far

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

    def generate_player_deck(self):
        """Generate a deck of randomly picked cards from the available card list."""
        for i in range(1, deck_size + 1):
            self.cards.append(self.randomiser(1, 1))
        self.shuffle()  # Optional: Shuffle the deck after generation
    
    def get_deck_info(self):
        """Return a string of the current deck information."""
        deck_info = ""
        i = 0
        for card in self.cards:
            deck_info += f"Card {i}:\n{card.get_card_info()}"
            i += 1
        return deck_info
    
    def generate_enemy_deck(self, matches_played: int, current_tier: int):
        tier_score = matches_played * 8
        print(f"DEBUG: Generating enemy deck with tier score {tier_score}.")
        current_tier_score = 0
        deck = []
        for i in range(0, 2):
            current_card = self.randomiser(current_tier, current_tier)
            self.cards.append(current_card)
            current_tier_score += current_card.tier
            print(f"DEBUG: Added card {current_card.name} with tier {current_card.tier}.")
            print(f"DEBUG: Current tier score: {current_tier_score}.")
        for i in range(0, 2):
            current_card = self.randomiser(current_tier - 1, current_tier - 1)
            self.cards.append(current_card)
            current_tier_score += current_card.tier
            print(f"DEBUG: Added card {current_card.name} with tier {current_card.tier}.")
            print(f"DEBUG: Current tier score: {current_tier_score}.")
        while current_tier_score < tier_score:
            current_card = self.randomiser(1, current_tier)
            self.cards.append(current_card)
            current_tier_score += current_card.tier
            print(f"DEBUG: Added card {current_card.name} with tier {current_card.tier}.")
            print(f"DEBUG: Current tier score: {current_tier_score}.")
        print(f"DEBUG: Enemy deck generated with {len(self.cards)} cards.")

# # Example usage
# deck = Deck()
# deck.generate_deck()
# print(f"Deck has {len(deck.cards)} cards.")
# for i in range(5):  # Draw some cards to see what we got
#     print(deck.draw().get_card_info())

'''
import random

def randomiser(baseLine, currentTier):
    if baseLine < 0:
        baseLine = 0
    chosenCard = random.randrange(baseLine, currentTier*5)
    if (chosenCard == 18) or (chosenCard == 19) or (chosenCard == 23) or (chosenCard == 24):
        specialCheck = random.randrange(0, 100)
        if (specialCheck != 69):
            chosenCard -= random.randrange(1, 4)
    return chosenCard

def cardCreator(matchesPlayed, currentTier):
    currentCard = 0
    tierScore = matchesPlayed*8
    currentTierScore = 0
    deck = list()
    for i in range(0, 2):
        currentCard = randomiser(currentTier *5 - 5, currentTier)
        deck.append(currentCard)
        currentTierScore += currentCard / 5
    for i in range(0, 2):
        currentCard = randomiser((currentTier -1) * 5 - 5, currentTier - 1)
        deck.append(currentCard)
        currentTierScore += currentCard / 5
    while currentTierScore < tierScore:
        currentCard = randomiser(0, currentTier)
        deck.append(currentCard)
        currentTierScore += currentCard / 5
    return deck

deck = cardCreator(5, 5)
for i in (deck):
    print(i)

'''