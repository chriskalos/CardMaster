from Deck import Deck


class User:
    def __init__(self):
        self.name = ""
        self.hp = 10
        self.mana = 0 # todo: Mana = current tier + 2
        self.alive_deck = Deck()
        self.dead_deck = Deck()
        self.cards_on_board = []
        self.hand = Deck()
        self.hand_size = 5

    def kill_card(self, card):
        self.dead_deck.cards.append(card)
        self.alive_deck.cards.remove(card)

    def play_card(self, card): # todo: Play card from hand into the turn, which in turn plays it into the match
        self.hand.cards.remove(card)
        self.mana -= card.tier
        self.dead_deck.cards.append(card)

    def play_turn(self):
        #todo: Call upon turn to take the cards from the board and play them
        pass

    def sacrifice_card(self, card): # Sacrifice 1 HP to send all cards on the board to the dead deck and redraw as many as they are from the alive deck
        # Find how many cards are on the board
        num_cards = len(self.cards_on_board)
        # For each card on the board, lose 1 HP and send it to the dead deck
        for card in self.cards_on_board:
            self.hp -= 1
            self.check_hp()
            self.dead_deck.cards.append(card)
            self.draw_card()
        self.cards_on_board.clear()

    def draw_card(self):
        if len(self.alive_deck.cards) > 0:
            card = self.alive_deck.draw()
            self.hand.cards.append(card)

    def check_hp(self):
        if self.hp <= 0:
            # todo: End round, player loses
            pass

    

class Player(User):
    def __init__(self):
        super().__init__()

        # Generate the player's deck only once at the start of the game
        """Generate a deck of randomly picked cards from the available card list."""
        for i in range(7): # Start with 7 cards
            self.alive_deck.cards.append(self.alive_deck.randomiser(1, 1))
        self.alive_deck.shuffle()  # Optional: Shuffle the deck after generation

    

class Enemy(User):
    def __init__(self, current_match: int, current_tier: int):
        super().__init__()

        tier_score = 2 + current_match * 5
        # The enemy should always have the maximum number of cards possible for the current match, as if they are a player buying every card in the store every round.
        print(f"DEBUG: Generating enemy deck with tier score {tier_score}.")
        current_tier_score = 0
        deck = []
        # The enemy gets 2 cards of the current tier, 2 cards of the previous tier, and then random cards until they reach the deck size indicated by tier_score.
        for i in range(2):
            current_card = self.alive_deck.randomiser(current_tier, current_tier)
            self.alive_deck.cards.append(current_card)
            current_tier_score += current_card.tier
            print(f"DEBUG: Added card {current_card.name} with tier {current_card.tier}.")
            print(f"DEBUG: Current tier score: {current_tier_score}.")
        for i in range(2):
            current_card = self.alive_deck.randomiser(current_tier - 1, current_tier - 1)
            self.alive_deck.cards.append(current_card)
            current_tier_score += current_card.tier
            print(f"DEBUG: Added card {current_card.name} with tier {current_card.tier}.")
            print(f"DEBUG: Current tier score: {current_tier_score}.")
        while current_tier_score < tier_score:
            current_card = self.alive_deck.randomiser(1, current_tier)
            self.alive_deck.cards.append(current_card)
            current_tier_score += current_card.tier
            print(f"DEBUG: Added card {current_card.name} with tier {current_card.tier}.")
            print(f"DEBUG: Current tier score: {current_tier_score}.")
        print(f"DEBUG: Enemy deck generated with {len(self.alive_deck.cards)} cards.")