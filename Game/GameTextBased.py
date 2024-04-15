from GameManager import GameManager

def display_card(card):
    print(card.get_card_info())

def get_user_option(string: str):
    option = input(string)
    return option

def show_player_deck():
        print("Player's Deck:")
        print(game_manager.player.alive_deck)

def show_board():
    print("Board:")
    # Add code to display the current state of the board

def end_turn():
    print("Ending turn...")
    # Add code to handle the logic for ending the turn

def battle():
    # game_manager.start_battle()
    def select_card():
        selected_card = get_user_option("Enter the number of the card you want to select: ")
        if selected_card.isdigit():
            selected_card = int(selected_card)
            if 0 <= selected_card < len(game_manager.player.alive_deck.cards):
                card = game_manager.player.alive_deck.cards[selected_card]
                print(f"Selected card: {card.get_card_info()}")
                option = get_user_option("Enter your option (1: Play card, 2: Go back): ")
                if option == "1":
                    # Add code to play the selected card on the board
                    print(f"Played {game_manager.player.alive_deck.cards[selected_card].name} on the board.")
                elif option == "2":
                    return
                else:
                    print("Invalid option")
            else:
                print("Invalid card number")
        else:
            print("Invalid input")

    option = get_user_option("Enter your option (1: Show player deck, 2: Show board, 3: End turn):")

    if option == "1":
        print(game_manager.player.alive_deck)
        option = get_user_option("Enter your option (1: Select card, 2: Go back): ")
        select_card()

    elif option == "2":
        show_board()
    elif option == "3":
        end_turn()
    else:
        print("Invalid option")

game_manager = GameManager()

name = input("Enter your name: ")
game_manager.player.name = name

while True:
    
    option = get_user_option("Enter your option (1: Start a battle, 2: Check deck, 3: quit): ")

    if option == "1":
        # Start a battle
        game_manager.start_match()
        battle()
    elif option == "2":
        # Check deck
        print(game_manager.player.alive_deck)
    elif option == "3":
        # Exit
        print("Exiting the game...")
        break
    else:
        print("Invalid option")
