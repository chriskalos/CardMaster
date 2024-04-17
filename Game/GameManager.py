from User import Player, Enemy
from Match import Match

class GameManager:
    def __init__(self):
        self.player = Player() # Gives the player a deck and draws 7 cards
        self.current_match_number = 0
        self.tier = 1
        self.player_wins = 0
        self.player_losses = 0
        self.current_match = None

    def record_win(self):
        """Record a win for the player."""
        self.player_wins += 1

    def record_loss(self):
        """Record a loss for the player."""
        self.player_losses += 1

    def start_match(self):
        """Start a new match."""

        self.current_match_number += 1
        # Increase the tier every 2 matches
        if self.current_match_number % 2 == 0:
            self.tier += 1
        # Make a new enemy for each round
        enemy = Enemy(self.current_match_number, self.tier)
        enemy.mana = self.tier + 2

        self.current_match = Match(self.tier, self.player, enemy)

        self.current_match.enemy.mana = self.tier + 2

        for i in range(self.player.hand_size):
            self.player.draw_card()
        for i in range(self.current_match.enemy.hand_size):
            self.current_match.enemy.draw_card()

        if self.current_match.phase.name == "DRAW":
            self.current_match.cycle_phase()
        else:
            print("Error: Match did not start in DRAW phase.")

    def get_game_stats(self):
        """Return a string of the current game statistics."""
        stats = (
            f"Matches: {self.current_match_number}\n"
            f"Tier: {self.tier}\n"
            f"Wins: {self.player_wins}\n"
            f"Losses: {self.player_losses}"
        )
        return stats