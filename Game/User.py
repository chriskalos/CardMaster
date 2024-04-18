import copy
import uuid

from Card import Deck


class User:
    def __init__(self, name: str, mode: str):
        self.name = name
        self.mode = mode
        self.hp = 10
        self.mana = 0  # Mana = current tier + 2, given by Match
        self.alive_deck = Deck()
        self.dead_deck = Deck()
        self.cards_on_board = Deck()
        self.hand = Deck()
        self.hand_size = 5

    def kill_card(self, card):
        self.dead_deck.cards.append(card)
        self.alive_deck.cards.remove(card)

    def play_card(self, card):
        if self.mana > 0:
            self.mana -= card.tier
            self.cards_on_board.cards.append(card)
            self.hand.cards.remove(card)
            self.print_debug(f"play_card: Playing card {card.name} with tier {card.tier}.")
            self.print_debug(f"play_card: Hand before playing card with UUID {card.uuid}:")
            self.print_debug(str(self.hand))
            self.print_debug(f"play_card: Cards on board before playing card with UUID {card.uuid}:")
            self.print_debug(str(self.cards_on_board))
            self.print_debug(f"play_card: Hand after playing card with UUID {card.uuid}:")
            self.print_debug(str(self.hand))
            self.print_debug(f"play_card: Cards on board after playing card with UUID {card.uuid}:")
            self.print_debug(str(self.cards_on_board))
            self.print_debug(f"play_card: Card {card.name} played. Mana remaining: {self.mana}.")
            return True
        else:
            print("No mana to play a card.")
            return False

    # Sacrifice 1 HP to send all cards on the board to the dead deck and redraw as many as they are from the alive deck
    def sacrifice_card(self, card):
        # Find how many cards are on the board
        num_cards = len(self.cards_on_board.cards)
        # For each card on the board, lose 1 HP and send it to the dead deck
        for card in self.cards_on_board.cards:
            self.hp -= 1
            self.check_hp()
            self.dead_deck.cards.append(card)
            self.draw_card()
        self.cards_on_board.cards.clear()

    def draw_card(self):
        print(f"AAAAAAAAAAAAAAAAAAAAAAAAA: {len(self.alive_deck.cards)}")
        if len(self.alive_deck.cards) > 0:
            card = self.alive_deck.draw()
            self.hand.cards.append(card)
        else:
            print("No cards left in the deck.")

    def check_hp(self):
        if self.hp <= 0:
            # todo: End round, player loses
            pass

    def create_new_card(self, lowest_tier: int, highest_tier: int):
        new_card = copy.copy(self.alive_deck.randomiser(lowest_tier, highest_tier))
        new_card.uuid = uuid.uuid4()
        return new_card

    def print_debug(self, message: str):
        if self.mode == "debug":
            print(f"DEBUG User {self.name}: {message}")
    

class Player(User):
    def __init__(self, name: str, mode: str = 'player'):
        super().__init__(name, mode)

        self.alive_deck.owner = self
        self.dead_deck.owner = self
        self.cards_on_board.owner = self

        # Generate the player's deck only once at the start of the game
        """Generate a deck of randomly picked cards from the available card list."""
        for i in range(7):  # Start with 7 cards
            new_card = self.create_new_card(1, 1)
            self.alive_deck.cards.append(new_card)
        self.alive_deck.shuffle()  # Optional: Shuffle the deck after generation

    

class Enemy(User):
    def __init__(self, current_match: int, current_tier: int, name: str = 'Enemy', mode: str = 'enemy'):
        super().__init__(name, mode)

        self.alive_deck.owner = self
        self.dead_deck.owner = self
        self.cards_on_board.owner = self

        tier_score = 2 + current_match * 5
        # The enemy should always have the maximum number of cards possible for the current match, as if they are a player buying every card in the store every round.
        self.print_debug(f"Generating enemy deck with tier score {tier_score}.")
        current_tier_score = 0
        deck = []
        # The enemy gets 2 cards of the current tier, 2 cards of the previous tier, and then random cards until they reach the deck size indicated by tier_score.
        for i in range(2):
            current_card = self.create_new_card(current_tier, current_tier)
            self.alive_deck.cards.append(current_card)
            current_tier_score += current_card.tier
            self.print_debug(f"Added card {current_card.name} with tier {current_card.tier}.")
            self.print_debug(f"Current tier score: {current_tier_score}.")
        for i in range(2):
            current_card = self.create_new_card(current_tier - 1, current_tier -1)
            self.alive_deck.cards.append(current_card)
            current_tier_score += current_card.tier
            self.print_debug(f"Added card {current_card.name} with tier {current_card.tier}.")
            self.print_debug(f"Current tier score: {current_tier_score}.")
        while current_tier_score < tier_score:
            current_card = self.create_new_card(1, current_tier)
            self.alive_deck.cards.append(current_card)
            current_tier_score += current_card.tier
            self.print_debug(f"Added card {current_card.name} with tier {current_card.tier}.")
            self.print_debug(f"Current tier score: {current_tier_score}.")
            self.print_debug(f"Enemy deck generated with {len(self.alive_deck.cards)} cards.")

    def play_turn(self):
        # Sort the hand by tier in descending order to try playing powerful cards first
        self.hand.cards.sort(key=lambda x: x.tier, reverse=True)
        played_cards = self.ai(self.mana, self.hand.cards)
        for card in played_cards:
            self.play_card(card)

    def ai(self, totalMana, hand):
        if totalMana == 0 or not hand:
            return []

        # Consider the most powerful card first (already sorted)
        current_card = hand[0]

        # If the card's mana cost is exactly the totalMana, or it fits within the mana, play it
        if current_card.tier <= totalMana:
            # Include this card in the selection and see if more can be played
            with_card = [current_card] + self.ai(totalMana - current_card.tier, hand[1:])
            # Also consider not playing this card and see which option is better
            without_card = self.ai(totalMana, hand[1:])

            # Choose the option that uses the most mana efficiently or maximizes the number of cards played
            if sum(card.tier for card in with_card) > sum(card.tier for card in without_card):
                return with_card
            else:
                return without_card
        else:
            # Skip this card as it's too costly to play
            return self.ai(totalMana, hand[1:])
