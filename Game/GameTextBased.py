from math import e
from GameManager import GameManager
import random

game_manager = GameManager()
game_manager.instantiate_player_deck()  # Create the initial deck
game_manager.instantiate_enemy_deck()  # Create the enemy deck

def display_card(card):
    print(card.get_card_info())

def display_deck(deck):
    for card in deck.cards:
        display_card(card)
        print()

def get_user_option():
    option = input("Enter your option (1: display deck, 2: display enemy's deck): ")
    return option

option = get_user_option()

if option == "1":
    display_deck(game_manager.player_deck)
elif option == "2":
    display_deck(game_manager.enemy_deck)
else:
    print("Invalid option")
