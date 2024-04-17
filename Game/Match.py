from enum import Enum, auto
from User import Enemy, Player

class Phase(Enum):
    DRAW = 1
    PLAY = 2
    ENEMY_PLAY = 3
    EFFECTS = 4
    ATTACKS = 5

class Match:
    def __init__(self, tier: int, player: Player, enemy: Enemy):
        self.tier = tier
        self.player = player
        self.enemy = enemy
        self.turn = 1
        self.player_score = 0
        self.enemy_score = 0
        self.phase = Phase.DRAW  # Initialize the phase to DRAW
        self.perform_phase()

        self.update_mana()
        # print(f"DEBUG: self.player.alive_deck.cards[0]: {self.player.alive_deck.cards[0]}")

    def update_mana(self):
        self.player.mana = self.tier + 2
        self.enemy.mana = self.tier + 2

    def activate_effects(self):
        # Take the maximum of player's cards on board vs enemy's cards on board
        max_hands = max(len(self.player.cards_on_board.cards), len(self.enemy.cards_on_board.cards))
        for i in range(max_hands):
            if i < max_hands:
                # If there is a card, activate the effect
                if i < len(self.player.cards_on_board.cards):
                    print(f"DEBUG: Activating player card {self.player.cards_on_board.cards[i].name}.")
                    self.player.cards_on_board.cards[i].activate_effect(i, self.player.cards_on_board,
                                                                        self.enemy.cards_on_board)
                if i < len(self.enemy.cards_on_board.cards):
                    print(f"DEBUG: Activating enemy card {self.enemy.cards_on_board.cards[i].name}.")
                    self.enemy.cards_on_board.cards[i].activate_effect(i, self.enemy.cards_on_board,
                                                                       self.player.cards_on_board)

        # self.cycle_phase()

    def cycle_phase(self):
        """Cycle the phase to the next phase."""
        if self.phase == Phase.DRAW:
            self.phase = Phase.PLAY
        elif self.phase == Phase.PLAY:
            self.phase = Phase.ENEMY_PLAY
        elif self.phase == Phase.ENEMY_PLAY:
            self.phase = Phase.EFFECTS
        elif self.phase == Phase.EFFECTS:
            self.phase = Phase.ATTACKS
        elif self.phase == Phase.ATTACKS:
            self.phase = Phase.DRAW
        self.perform_phase()

    def perform_attacks(self):
        # Take the maximum of player's hands on board vs enemy's hands on board
        print(f"DEBUG: Player cards on board BEFORE ATTACKS: {self.player.cards_on_board}")
        print(f"DEBUG: Enemy cards on board BEFORE ATTACKS: {self.enemy.cards_on_board}")

        max_hands = max(len(self.player.cards_on_board.cards), len(self.enemy.cards_on_board.cards))
        for i in range(max_hands):
            if i < len(self.enemy.cards_on_board.cards):
                print(f"DEBUG: Enemy attacking with card {self.enemy.cards_on_board.cards[i].name}.")
                self.enemy.cards_on_board.cards[i].perform_attack(i, self.player.cards_on_board)
            if i < len(self.player.cards_on_board.cards):
                print(f"DEBUG: Player attacking with card {self.player.cards_on_board.cards[i].name}.")
                self.player.cards_on_board.cards[i].perform_attack(i, self.enemy.cards_on_board)

        print(f"DEBUG: Player cards on board AFTER ATTACKS: {self.player.cards_on_board}")
        print(f"DEBUG: Enemy cards on board AFTER ATTACKS: {self.enemy.cards_on_board}")

    def draw_new_cards(self):
        # Clear dead cards from the board
        player_dead_cards = []
        for card in self.player.cards_on_board.cards:
            if card.hp <= 0:
                self.player.dead_deck.cards.append(card)
                player_dead_cards.append(card)

        enemy_dead_cards = []
        for card in self.enemy.cards_on_board.cards:
            if card.hp <= 0:
                self.enemy.dead_deck.cards.append(card)
                enemy_dead_cards.append(card)

        # Remove dead cards from the board
        for card in player_dead_cards:
            self.player.cards_on_board.cards.remove(card)

        for card in enemy_dead_cards:
            self.enemy.cards_on_board.cards.remove(card)

        # Draw cards for the player and the enemy until they have 5 in hand
        while len(self.player.hand.cards) < self.player.hand_size:
            self.player.draw_card()
        while len(self.enemy.hand.cards) < self.enemy.hand_size:
            self.enemy.draw_card()


    def perform_phase(self):
        if self.phase == Phase.DRAW:
            self.draw_new_cards()
            print("DEBUG: Phase is now DRAW.")
            self.cycle_phase()  # You shouldn't be able to play cards during the draw phase so cycle to the next phase automatically.
        elif self.phase == Phase.PLAY:
            print("DEBUG: Phase is now PLAY.")
        elif self.phase == Phase.ENEMY_PLAY:
            print("DEBUG: Phase is now ENEMY_PLAY.")
            self.enemy.play_turn()
        elif self.phase == Phase.EFFECTS:
            print("DEBUG: Phase is now EFFECTS.")
            self.activate_effects()
        elif self.phase == Phase.ATTACKS:
            print("DEBUG: Phase is now ATTACKS.")
            self.perform_attacks()
            self.update_mana()
            self.turn += 1
        else:
            print("DEBUG: ERROR: Phase is not a valid phase.")
