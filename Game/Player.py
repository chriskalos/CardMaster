class Player:
    def __init__(self):
        self.name = ""
        self.hp = 10
        self.mana = 0
        self.alive_deck = []
        self.dead_deck = []
        self.cards_on_board = []
        self.hand = []
    
    def create_deck(self, deck):
        self.alive_deck = deck

    def kill_card(self, card):
        self.dead_deck.append(card)
        self.alive_deck.remove(card)

    def play_card(self, card): # todo: Play card from hand into the turn, which in turn plays it into the match
        self.hand.remove(card)
        self.mana -= card.tier
        self.dead_deck.append(card)

    def play_turn(self):
        #todo: Call upon turn to take the cards from the board and play them
        pass

    def sacrifice_card(self, card): # Sacrifice 1 HP to send all cards on the board to the dead deck and redraw as many as they are from the alive deck
        # Find how many cards are on the board
        num_cards = len(self.cards_on_board)
        # For each card on the board, lose 1 HP and send it to the dead deck
        for card in self.cards_on_board:
            self.hp -= 1
            self.check_hp()
            self.dead_deck.append(card)
            self.draw_card()
        self.cards_on_board.clear()

    def draw_card(self):
        # todo: Draw card
        pass

    def check_hp(self):
        if self.hp <= 0:
            # todo: End round, player loses
            pass

class Enemy(Player):
    def __init__(self):
        super().__init__()

    def play_turn(self):
        # todo: Implement AI to play the turn from TemporaryFunctions.py
        pass