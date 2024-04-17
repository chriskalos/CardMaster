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

    def update_mana(self):
        self.player.mana = self.tier + 2
        self.enemy.mana = self.tier + 2

    def cycle_phase(self):
        """Cycle the phase to the next phase."""
        if self.phase == Phase.DRAW:
            self.phase = Phase.PLAY
        elif self.phase == Phase.PLAY:
            self.enemy.play_turn()
            self.phase = Phase.EFFECTS
        elif self.phase == Phase.EFFECTS:
            self.phase = Phase.ATTACKS
        elif self.phase == Phase.ATTACKS:
            self.update_mana()
            self.phase = Phase.DRAW
            self.turn += 1
            self.update_mana()
