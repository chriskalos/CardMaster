from User import Player, Enemy
from Match import Match

class GameManager:
    def __init__(self, debug_mode=False):
        self.debug_mode = debug_mode
        self.game_over = False
        self.current_match_number = 0
        self.tier = 1
        self.player_wins = 0
        self.player_losses = 0
        self.current_match = None
        self.debug_mode = False
        self.player = None

        self.start_match()

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
            if self.tier > 5:
                self.tier = 5
        # Make a new enemy for each round
        deck_size = self.current_match_number * 2 + 10
        if self.debug_mode:
            self.player = Player(self.current_match_number, self.tier, 'Player', deck_size, 'debug')
        else:
            self.player = Player(self.current_match_number, self.tier, 'Player', deck_size, 'player')
        enemy = None
        if self.debug_mode:
            enemy = Enemy(self.current_match_number, self.tier, deck_size, 'Enemy', 'debug')
        else:
            enemy = Enemy(self.current_match_number, self.tier, deck_size, 'Enemy', 'enemy')
        self.current_match = Match(self.tier, self.player, enemy)

    def check_match(self):
        """Check if the match is over."""
        if self.current_match.match_over:
            self.end_match()
            return True
        else:
            return False

    def end_match(self):
        """End the current match."""
        if self.current_match.winner == self.player:
            self.record_win()
            self.start_match()
        else:
            self.record_loss()
            self.game_over = True

    def get_game_stats(self):
        """Return a string of the current game statistics."""
        stats = (
            f"Matches: {self.current_match_number}\n"
            f"Tier: {self.tier}\n"
            f"Wins: {self.player_wins}\n"
            f"Losses: {self.player_losses}"
        )
        return stats
