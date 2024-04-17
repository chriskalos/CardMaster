from enum import Enum
from User import Enemy, Player

class Phase(Enum):
    DRAW = 1
    PLAY = 2
    EFFECTS = 3
    ATTACKS = 4

class Match:
    def __init__(self, tier: int, player: Player, enemy: Enemy):
        self.tier = tier
        self.player = player
        self.enemy = enemy
        self.turn = 1
        self.player_score = 0
        self.enemy_score = 0
        self.phase = Phase.DRAW  # Initialize the phase to DRAW

        self.update_mana()
        print(f"DEBUG: self.player.alive_deck.cards[0]: {self.player.alive_deck.cards[0]}")

    def update_mana(self):
        self.player.mana = self.tier + 2
        self.enemy.mana = self.tier + 2

    def activate_effects(self):
        # Take the maximum of player's hands on board vs enemy's hands on board
        max_hands = max(len(self.player.cards_on_board.cards), len(self.enemy.cards_on_board.cards))
        for i in range(max_hands):
            if i < max_hands:
                print(f"DEBUG: Activating player card {self.player.cards_on_board.cards[i].name}.")
                self.player.cards_on_board.cards[i].activate_effect(i, self.player.cards_on_board, self.enemy.cards_on_board)
            if i < max_hands:
                print(f"DEBUG: Activating player card {self.player.cards_on_board.cards[i].name}.")
                self.enemy.cards_on_board.cards[i].activate_effect(i, self.enemy.cards_on_board, self.player.cards_on_board)
        self.cycle_phase()

    def cycle_phase(self):
        """Cycle the phase to the next phase."""
        if self.phase == Phase.DRAW:
            self.phase = Phase.PLAY
        elif self.phase == Phase.PLAY:
            self.phase = Phase.EFFECTS
        elif self.phase == Phase.EFFECTS:
            self.phase = Phase.ATTACKS
        elif self.phase == Phase.ATTACKS:
            self.phase = Phase.DRAW
        self.check_phase()

    def perform_attacks(self):
        # Take the maximum of player's hands on board vs enemy's hands on board
        max_hands = max(len(self.player.cards_on_board.cards), len(self.enemy.cards_on_board.cards))
        for i in range(max_hands):
            if i < max_hands:
                print(f"DEBUG: Player attacking with card {self.player.cards_on_board.cards[i].name}.")
                self.player.cards_on_board.cards[i].perform_attack(i, self.enemy.cards_on_board)
            if i < max_hands:
                print(f"DEBUG: Enemy attacking with card {self.enemy.cards_on_board.cards[i].name}.")
                self.enemy.cards_on_board.cards[i].perform_attack(i, self.player.cards_on_board)

    def draw_new_cards(self):
        # Clear dead cards from the board
        for card in self.player.cards_on_board.cards:
            if card.hp <= 0:
                self.player.cards_on_board.cards.remove(card)
                self.player.dead_deck.cards.append(card)
        for card in self.enemy.cards_on_board.cards:
            if card.hp <= 0:
                self.enemy.cards_on_board.cards.remove(card)
                self.enemy.dead_deck.cards.append(card)

        # Draw cards for the player and the enemy until they have 5 in hand
        while len(self.player.hand.cards) < 5:
            self.player.draw_card()
        while len(self.enemy.hand.cards) < 5:
            self.enemy.draw_card()


    def check_phase(self):
        if self.phase == Phase.DRAW:
            print("DEBUG: Phase is now DRAW.")
        elif self.phase == Phase.PLAY:
            print("DEBUG: Phase is now PLAY.")
        elif self.phase == Phase.EFFECTS:
            self.enemy.play_turn()
            print("DEBUG: Phase is now EFFECTS.")
            self.activate_effects()
        elif self.phase == Phase.ATTACKS:
            print("DEBUG: Phase is now ATTACKS.")
            self.perform_attacks()
            self.update_mana()
            self.turn += 1
        else:
            print("DEBUG: ERROR: Phase is not a valid phase.")
