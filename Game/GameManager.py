from User import Player, Enemy
from Match import Match

class GameManager:
    def __init__(self):
        self.current_match_number = 0
        self.tier = 1
        self.player_wins = 0
        self.player_losses = 0
        self.current_match = None
        self.debug_mode = False

        if self.debug_mode:
            self.player = Player('debug')
        else:
            self.player = Player('player')  # Gives the player a deck and draws 7 cards

    def enable_debug_mode(self):
        """Enable debug mode."""
        self.debug_mode = True

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
        enemy = Enemy(self.current_match_number, self.tier, 'Enemy', 'enemy')
        self.current_match = Match(self.tier, self.player, enemy)

    def get_game_stats(self):
        """Return a string of the current game statistics."""
        stats = (
            f"Matches: {self.current_match_number}\n"
            f"Tier: {self.tier}\n"
            f"Wins: {self.player_wins}\n"
            f"Losses: {self.player_losses}"
        )
        return stats
