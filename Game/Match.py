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