from GameManager import GameManager

game_manager = GameManager()
game_manager.instantiate_player_deck()  # Create the initial deck


def display_card(card):
    print(card.get_card_info())

def display_deck(deck):
    for card in deck.cards:
        display_card(card)
        print()

def get_user_option(string: str):
    option = input(string)
    return option

def show_player_deck():
        print("Player's Deck:")
        display_deck(game_manager.player_deck)

def show_board():
    print("Board:")
    # Add code to display the current state of the board

def end_turn():
    print("Ending turn...")
    # Add code to handle the logic for ending the turn

def select_card():
    selected_card = get_user_option("Enter the number of the card you want to select: ")
    if selected_card.isdigit():
        selected_card = int(selected_card)
        if 0 <= selected_card < len(game_manager.player_deck.cards):
            card = game_manager.player_deck.cards[selected_card]
            print(f"Selected card: {card.get_card_info()}")
            option = get_user_option("Enter your option (1: Play card, 2: Go back): ")
            if option == "1":
                # Add code to play the selected card on the board
                print(f"Played {game_manager.player_deck.cards[selected_card].name} on the board.")
            elif option == "2":
                battle()
            else:
                print("Invalid option")
        else:
            print("Invalid card number")
    else:
        print("Invalid input")

def battle():
    option = get_user_option("Enter your option (1: Show player deck, 2: Show board, 3: End turn):")

    if option == "1":
        game_manager.player_deck.get_deck_info()
        selected_card = get_user_option("Enter the number of the card you want to select: ")
        if selected_card.isdigit():
            selected_card = int(selected_card)
            if 0 <= selected_card < len(game_manager.player_deck.cards):
                card = game_manager.player_deck.cards[selected_card]
                print(f"Selected card: {card.get_card_info()}")
                option = get_user_option("Enter your option (1: Play card, 2: Go back): ")
                if option == "1":
                    # Add code to play the selected card on the board
                    print(f"Played {game_manager.player_deck.cards[selected_card].name} on the board.")
                elif option == "2":
                    battle()
                else:
                    print("Invalid option")
            else:
                print("Invalid card number")
        else:
            print("Invalid input")
    elif option == "2":
        show_board()
    elif option == "3":
        end_turn()
    else:
        print("Invalid option")


name = input("Enter your name: ")
game_manager.player.name = name

while True:
    game_manager.player.mana = game_manager.tier + 2 # Set the player's mana to the current tier + 2
    option = get_user_option("Enter your option (1: Start a battle, 2: Check deck, 3: quit): ")

    if option == "1":
        # Start a battle
        game_manager.matches += 1  # Increase the match count
        print(f"Starting battle number {game_manager.matches}...")
        game_manager.instantiate_enemy_deck()  # Create the enemy deck
        battle()
    elif option == "2":
        # Check deck
        display_deck(game_manager.player_deck)
    elif option == "3":
        # Exit
        print("Exiting the game...")
        break
    else:
        print("Invalid option")
