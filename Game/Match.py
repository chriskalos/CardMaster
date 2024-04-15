from enum import Enum
from Game.Board import Board
from Game.Player import Enemy, Player

class Phase(Enum):
    DRAW = 1
    PLAY = 2
    EFFECTS = 3
    ATTACKS = 4

class Match:
    def __init__(self, tier: int, player: Player, enemy: Enemy, turn: int, board: Board, player_score: int, enemy_score:int):
        self.tier = tier
        self.player = player
        self.enemy = enemy
        self.turn = turn
        self.board = board
        self.player_score = player_score
        self.enemy_score = enemy_score
        self.phase = Phase.DRAW  # Initialize the phase to DRAW