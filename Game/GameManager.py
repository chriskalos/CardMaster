from Deck import Deck
from Player import Player

class GameManager:
    def __init__(self):
        self.matches = 1
        self.tier = 1
        self.player_wins = 0
        self.player_losses = 0
        self.player_deck = Deck()
        self.enemy_deck = Deck() # todo: Enemy deck will change every match

    def increase_match(self):
        """Increase the match count and adjust tier accordingly."""
        self.matches += 1
        if self.matches % 2 == 0:
            self.increase_tier()

    def increase_tier(self):
        """Increase the player's tier."""
        self.tier += 1

    def instantiate_player_deck(self):
        """Instantiate the player's deck from the Deck class."""
        self.player_deck = Deck()
        self.player_deck.generate_player_deck()

    def instantiate_enemy_deck(self):
        """Instantiate the enemy's deck from the Deck class."""
        print("DEBUG: Generating enemy deck")
        print(f"DEBUG: Matches: {self.matches}, Tier: {self.tier}")
        self.enemy_deck = Deck()
        self.enemy_deck.generate_enemy_deck(self.matches, self.tier)

    def update_enemy_deck(self, new_enemy_deck: Deck):
        """Update the enemy's deck with a new deck."""
        self.enemy_deck = new_enemy_deck

    def record_win(self):
        """Record a win for the player."""
        self.player_wins += 1

    def record_loss(self):
        """Record a loss for the player."""
        self.player_losses += 1

    def get_game_stats(self):
        """Return a string of the current game statistics."""
        stats = (
            f"Matches: {self.matches}\n"
            f"Tier: {self.tier}\n"
            f"Wins: {self.player_wins}\n"
            f"Losses: {self.player_losses}"
        )
        return stats