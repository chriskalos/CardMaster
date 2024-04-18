import os
import random
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Optional
from PySide6.QtGui import QPixmap, QImage

class Deck:
    def __init__(self):
        self.cards = []  # Start with an empty list of cards
        self.owner = None

    def shuffle(self):
        """Shuffle the deck of cards."""
        random.shuffle(self.cards)

    def randomiser(self, lowest_tier: int, highest_tier: int):
        # print(f"### - Lowest tier: {lowest_tier}, Highest tier: {highest_tier}")
        if lowest_tier < 1:
            lowest_tier = 1
        if highest_tier < 1:
            highest_tier = 1
        if random.random() < 0.05 and highest_tier > 3:
            chosen_card = random.choice(
                [card for card in cards_list if card.tier <= highest_tier and card.card_class.name == "RARE"])
        else:
            chosen_card = random.choice([card for card in cards_list if
                                         card.tier >= lowest_tier and card.tier <= highest_tier and card.card_class.name != "RARE"])
        return chosen_card

    # Return a list of copies of all cards in the game
    def get_all_cards(self):
        return [card for card in cards_list]

    def draw(self):
        """Draw a card from the deck, removing it from the deck."""
        if not self.cards:
            raise ValueError("No cards left in the deck!")
        return self.cards.pop()

    def __str__(self):
        """Return a string of the current deck information."""
        deck_info = ""
        i = 0
        for card in self.cards:
            deck_info += f"Card {i}:\n{card}"
            i += 1
        return deck_info

class CardClass(Enum):
    BRAWLER = auto()
    ARCHER = auto()
    MAGE = auto()
    RARE = auto()

class CardColor(Enum):
    GREEN = auto()
    BLUE = auto()
    PURPLE = auto()
    YELLOW = auto()
    RED = auto()

class Card(ABC):
    """An abstract base class representing a card in the game.

    Attributes:
        name (str): The name of the card.
        description (str): The description of the card.
        tier (int): The tier of the card (1 to 5)
        hp (int): The health points of the card.
        attack (int): The attack points of the card.
        card_class (CardClass): The class of the card (Brawler, Archer, Mage, Rare).
        effect_description (str, optional): The description of the card's special effect.
        image (QPixmap): The image of the card.

    Methods:
        activate_effect(): Method to activate the card's special effect.
        perform_attack(target): Method to perform an attack on a target.
        die(): Method to handle the card's death.
    """

    def __init__(self, name: str, description: str, tier: int, hp: int, attack: int, card_class: CardClass, effect_description: Optional[str] = "No special effect"):
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        if not isinstance(description, str):
            raise TypeError("Description must be a string.")
        if not isinstance(tier, int):
            raise TypeError("Tier must be an integer.")
        if not (1 <= tier <= 5):
            raise ValueError("Tier must be between 1 and 5.")
        if not isinstance(hp, int):
            raise TypeError("HP must be an integer.")
        if not isinstance(attack, int):
            raise TypeError("Attack must be an integer.")
        if not isinstance(card_class, CardClass):
            raise TypeError("Card class must be an instance of CardClass.")
        if not isinstance(effect_description, str):
            raise TypeError("Effect description must be a string.")

        self.uuid = None
        self.name = name
        self.description = description
        self.tier = tier
        self.hp = hp
        self.attack = attack
        self.card_class = CardClass(card_class)
        self.color = CardColor(list(CardColor)[self.tier-1])
        self.effect_description = effect_description
        # Correctly form the path to the image
        image_path = os.path.join(os.getcwd(), 'img', f'{self.name.lower()}.png')
        self.image = QImage(str(image_path))
        # if self.image.isNull():
        #     print(f"Failed to load image from {image_path}")
        # else:
        #     print(f"Image loaded successfully from {image_path}")

        # Status effects
        self.attack_times = 1  # How many times the unit attacks per turn
        self.shield = False  # Whether the unit can take the next instance of damage
        self.life_steal = False  # Whether the unit heals for the amount of damage it deals
        self.frozen = False  # Whether the unit is frozen and cannot attack or use its effect

        # Temporary stats pointing to the original stats, for effects that last for the duration of the turn
        self.temp_attack = self.attack
        self.temp_hp = self.hp

    @abstractmethod
    # Optional attribute "target" for cards that need to target a specific card
    def activate_effect(self, position: int, friendly_board: Deck, enemy_board: Deck):
        """Method to activate the card's special effect"""
        pass

    def reset_temp_stats(self):
        """Method to reset the temporary stats of the card"""
        self.attack = self.temp_attack
        self.hp = self.temp_hp

    def perform_attack(self, position: int, enemy_board: Deck):
        """Method to perform an attack on a target"""
        # Check if the target is the enemy player or a card
        target = None
        if enemy_board.cards[position] is None:
            target = enemy_board.owner
        else:
            target = enemy_board.cards[position]

        # Check if the card is frozen or has a shield
        if self.frozen:
            print(f"DEBUG {self.name}: Target {self.name} is frozen and cannot attack.")
            self.frozen = False
            return
        if target.shield:
            print(f"DEBUG {self.name}: Target {target.name} has a shield and takes no damage.")
            target.shield = False
            return

        # Perform the attack
        damage_dealt = 0
        for i in range(self.attack_times):
            damage_dealt += self.attack
            print(f"DEBUG {self.name}: Attacks {target.name} for {self.attack} damage! Run: {i+1}/{self.attack_times}")
            target.hp -= self.attack
            print(f"DEBUG {target.name}: HP: {target.hp}")

        if self.life_steal:
            self.hp += damage_dealt
            print(f"DEBUG {self.name}: Heals for {damage_dealt} HP due to life steal.")
            self.life_steal = False
            print(f"DEBUG {self.name}: Disabled life steal.")

        # target.check_hp()
        target = None

    def die(self):
        """Method to handle the card's death"""
        print(f"{self.name} has died.")
        # Destroy object
        # del self

    def check_hp(self):
        """Method to check the card's health points and handle death if necessary"""
        if self.hp <= 0:
            self.die()

    def __str__(self):
        return (
            f"-=| Card Information| =-\n"
            f"UUID: {self.uuid}\n"
            f"Name: {self.name}\n"
            f"Description: {self.description}\n"
            f"Tier: {self.tier}\n"
            f"HP: {self.hp}\n"
            f"Attack: {self.attack}\n"
            f"Card Class: {self.card_class.name}\n"
            f"Color: {self.color.name}\n"
            f"Effect Description: {self.effect_description}\n\n"
        )

# Cards without effects need to be instantiated using SimpleCard
class SimpleCard(Card):
    def activate_effect(self, position: int, friendly_board: Deck, enemy_board: Deck):
        """This card has no special effect."""
        pass

# Specific card implementations for special effects
class Grag(Card):
    def activate_effect(self, position: int, friendly_board: Deck, enemy_board: Deck):
        print(f"DEBUG Grag: Add 2 health to the unit to the left")
        if self.frozen:
            print(f"DEBUG Grag: Target {self.name} is frozen and cannot attack.")
            self.frozen = False
            return
        if position > 0:
            target = friendly_board.cards[position-1]
            target.hp += 2
        # target.check_hp()

class Pew(Card):
    def activate_effect(self, position, friendly_board: Deck, enemy_board: Deck):
        if self.frozen:
            print(f"DEBUG Pew: Target {self.name} is frozen and cannot attack.")
            self.frozen = False
            return
        print(f"DEBUG Pew: Deal 2 damage to the unit in front of it")
        target = enemy_board.cards[position]
        if not target.shield:
            target.hp -= 2
        # target.check_hp()

class Rasmus(Card):
    def activate_effect(self, position, friendly_board: Deck, enemy_board: Deck):
        print(f"DEBUG Rasmus: Make the unit to the left attack again")
        if self.frozen:
            print(f"DEBUG Rasmus: Target {self.name} is frozen and cannot attack.")
            self.frozen = False
            return
        if position > 0:
            target = friendly_board.cards[position-1]
            target.attack_times += 1

class Bank(Card):
    def activate_effect(self, position, friendly_board: Deck, enemy_board: Deck):
        print(f"DEBUG Bank: For every unit to his left, Bank gains 1 attack and 1 HP")
        if self.frozen:
            print(f"DEBUG Bank: Target {self.name} is frozen and cannot attack.")
            self.frozen = False
            return
        for i in range(position):
            self.attack += 1
            self.hp += 1

class PewPew(Card):
    def activate_effect(self, position, friendly_board: Deck, enemy_board: Deck):
        if self.frozen:
            print(f"DEBUG Pew Pew: Target {self.name} is frozen and cannot attack.")
            self.frozen = False
            return
        print(f"DEBUG Pew Pew: Deal 2 damage to the opposing unit")
        target = enemy_board.cards[position]
        if not target.shield:
            target.hp -= 2
        # target.check_hp()


class Boom(Card):
    def activate_effect(self, position, friendly_board: Deck, enemy_board: Deck):
        print(f"DEBUG Boom: Shoot opposing unit for 1 damage for each friendly unit on the board")
        if self.frozen:
            print(f"DEBUG Boom: Target {self.name} is frozen and cannot attack.")
            self.frozen = False
            return
        target = enemy_board.cards[position]
        if not target.shield:
            target.hp -= len(friendly_board.cards)
        # target.check_hp()

class Malik(Card):
    def activate_effect(self, position, friendly_board: Deck, enemy_board: Deck):
        print(f"DEBUG Malik: Unit to the left does not take the next instance of damage")
        if self.frozen:
            print(f"DEBUG Malik: Target {self.name} is frozen and cannot attack.")
            self.frozen = False
            return
        target = friendly_board.cards[position-1]
        target.shield = True

class Brap(Card):
    def activate_effect(self, position, friendly_board: Deck, enemy_board: Deck):
        print(f"DEBUG Brap: Attack the opposing unit.")
        # Doesn't need to check if frozen because attack does
        self.perform_attack(position, enemy_board)

class Cablooey(Card):
    def activate_effect(self, position, friendly_board: Deck, enemy_board: Deck):
        print(f"DEBUG Cablooey: Shoot opposing unit for 50% of its HP.")
        if self.frozen:
            print(f"DEBUG Cablooey: Target {self.name} is frozen and cannot attack.")
            self.frozen = False
            return
        target = enemy_board.cards[position]
        if not target.shield:
            target.hp -= target.hp // 2
        # target.check_hp()

class Catapulty(Card):
    def activate_effect(self, position, friendly_board: Deck, enemy_board: Deck):
        print(f"DEBUG Catapulty: Shoot the opposing unit for its own attack value.")
        if self.frozen:
            print(f"DEBUG Catapulty: Target {self.name} is frozen and cannot attack.")
            self.frozen = False
            return
        target = enemy_board.cards[position]
        if not target.shield:
            target.hp -= target.attack
        # target.check_hp()

class Nomnom(Card):
    def activate_effect(self, position, friendly_board: Deck, enemy_board: Deck):
        print(f"DEBUG Nomnom: "
              f"Unit to the left gains life steal for the duration of the turn. "
              f"Life steal heals the unit for the amount of damage it deals.")
        if self.frozen:
            print(f"DEBUG Nomnom: Target {self.name} is frozen and cannot attack.")
            self.frozen = False
            return
        target = friendly_board.cards[position-1]
        target.life_steal = True

class TimeLord(Card):
    def __init__(self, name: str, description: str, tier: int, hp: int, attack: int, card_class: CardClass, effect_description: str):
        super().__init__(name, description, tier, hp, attack, card_class, effect_description)
        self.condition = False
        self.temp_enemy = None
        self.turns_active = 0

    def activate_effect(self, position, friendly_board: Deck, enemy_board: Deck):
        print(f"DEBUG Time Lord: "
              f"If both this unit and the opposing unit are alive by the next turn, destroy the opposing unit.")
        if self.frozen:
            print(f"DEBUG Time Lord: Target {self.name} is frozen and cannot attack.")
            self.frozen = False
            return
        target = enemy_board.cards[position]
        self.turns_active += 1
        if self.temp_enemy is target and self.turns_active == 1:
            target.hp = 0
            # target.check_hp()
        else:
            self.temp_enemy = target
            self.turns_active = 0

class BigShot(Card):
    def activate_effect(self, position, friendly_board: Deck, enemy_board: Deck):
        print(f"DEBUG Big Shot: Shoot opposing unit for the combined attack of all friendly units on the board.")
        if self.frozen:
            print(f"DEBUG Big Shot: Target {self.name} is frozen and cannot attack.")
            self.frozen = False
            return
        total_attack = 0
        target = enemy_board.cards[position]
        for card in friendly_board.cards:
            total_attack += card.attack
        if not target.shield:
            target.hp -= total_attack
        # target.check_hp()

class IceCube(Card):
    def activate_effect(self, position, friendly_board: Deck, enemy_board: Deck):
        print(f"DEBUG Ice Cube: Freeze the opposing unit for the next turn.")
        if self.frozen:
            print(f"DEBUG Ice Cube: Target {self.name} is frozen and cannot attack.")
            self.frozen = False
            return
        target = enemy_board.cards[position]
        target.frozen = True

class Cheerleader(Card):
    def activate_effect(self, position, friendly_board: Deck, enemy_board: Deck):
        print(f"DEBUG Cheerleader: Give all friendly units on the board "
              f"+3 attack and +3 HP for the duration of the turn.")
        if not self.frozen:
            for card in friendly_board.cards:
                card.temp_attack += 3
                card.temp_hp += 3
        else:
            print(f"DEBUG Cheerleader: Target {self.name} is frozen and cannot attack.")
            self.frozen = False

class HungryAssassin(Card):
    def activate_effect(self, position, friendly_board: Deck, enemy_board: Deck):
        print(f"DEBUG Hungry Assassin: Sacrifice as much HP as the opposing unit's HP to destroy it.")
        if self.frozen:
            print(f"DEBUG Hungry Assassin: Target {self.name} is frozen and cannot attack.")
            self.frozen = False
            return
        target = enemy_board.cards[position]
        if target.shield:
            print(f"DEBUG Hungry Assassin: Target {target.name} has a shield and takes no damage.")
            target.shield = False
            return
        if self.hp >= target.hp:
            self.hp -= target.hp
            target.hp = 0
        # target.check_hp()

class Flea(Card):
    def activate_effect(self, position, friendly_board: Deck, enemy_board: Deck):
        print(f"DEBUG Flea: Deals fatal damage to the first target.")
        if self.frozen:
            print(f"DEBUG Flea: Target {self.name} is frozen and cannot attack.")
            self.frozen = False
            return
        target = enemy_board.cards[position]
        target.hp = 0
        # We do not want the target to check its HP we actually want it to just go to 0 HP


class BigGunga(Card):
    def activate_effect(self, position, friendly_board: Deck, enemy_board: Deck):
        print(f"DEBUG Big Gunga: This unit attacks the opposing unit. If the opposing unit dies from this attack, "
              f"gain half its stats.")
        if self.frozen:
            print(f"DEBUG Big Gunga: Target {self.name} is frozen and cannot attack.")
            self.frozen = False
            return
        target = enemy_board.cards[position]
        if not target.shield:
            self.perform_attack(position, enemy_board)
            if target.hp <= 0:
                    self.hp += target.hp // 2
                    self.attack += target.attack // 2
                    print(f"DEBUG Big Gunga: Gained {target.hp // 2} HP and "
                          f"{target.attack // 2} attack from {target.name}.")
        # target.check_hp()


class Sender(Card):
    def activate_effect(self, position, friendly_board: Deck, enemy_board: Deck):
        print(f"DEBUG Sender: Shoot the opposing unit for the combined attack and HP values of the unit to the left.")
        if self.frozen:
            print(f"DEBUG Sender: Target {self.name} is frozen and cannot attack.")
            self.frozen = False
            return
        target = enemy_board.cards[position]
        left = friendly_board.cards[position-1]
        if not target.shield:
            target.hp -= left.attack + left.hp
        # target.check_hp()

class RoyalSummoner(Card):
    def activate_effect(self, position, friendly_board: Deck, enemy_board: Deck):
        print(f"DEBUG Royal Summoner: Summon the unit to his left and add it to his right on the board.")
        if self.frozen:
            print(f"DEBUG Royal Summoner: Target {self.name} is frozen and cannot attack.")
            self.frozen = False
            return
        if position > 0:
            left = friendly_board.cards[position-1]
            friendly_board.cards.insert(position+1, left)

class Copycat(Card):
    def activate_effect(self, position, friendly_board: Deck, enemy_board: Deck):
        print(f"DEBUG Copycat: Gain 1 attack and 1 HP for every unit on the board.")
        # Permanently means for the duration of the match, not like forever
        for card in friendly_board.cards:
            card.temp_attack += 1
            card.temp_hp += 1
        for card in enemy_board.cards:
            card.temp_attack += 1
            card.temp_hp += 1

class UnceasingVoid(Card):
    def activate_effect(self, position, friendly_board: Deck, enemy_board: Deck):
        print(f"DEBUG Void: If this unit is on the board, you cannot die.")
        if friendly_board.owner.hp <= 0:
            friendly_board.owner.hp = 1


# List of all cards
cards_list = [
    SimpleCard("Greg", "Ooga booga", 1, 1, 5, CardClass.BRAWLER),
    SimpleCard("Grog", "Unga bunga", 1, 4, 2, CardClass.BRAWLER),
    Grag("Grag", "Gonk gonk", 1, 1, 2, CardClass.BRAWLER, "Heals the unit to his left by 2 HP out of the kindness of his heart"),
    Pew("Pew", "I am an archer. I go pew. Just once.", 1, 1, 1, CardClass.ARCHER, "Deals 2 damage to the unit in front of him. Pew!"),
    Rasmus("Rasmus", "I am Rasmus the Almighty. Tremble before me.", 1, 2, 2, CardClass.MAGE, "Inspires the unit to his left to attack twice."),
    SimpleCard("Bonk", "Bonk bonk", 2, 5, 6, CardClass.BRAWLER),
    Bank("Bank", "Cha-ching!", 2, 3, 3, CardClass.BRAWLER, "For every to his left, Bank gains 1 attack and 1 HP. We makin' bank!"),
    PewPew("Pew Pew", "I am an archer. I go pew pew. Simple as that.", 2, 1, 2, CardClass.ARCHER, "Damages the opposing unit twice, for 2 damage each time. Pew pew!"),
    Boom("Boom", "In contrast to my name, I am a very calm and collected individual.", 2, 1, 1, CardClass.ARCHER, "For each friendly unit on the board, deal 1 damage to the opposing unit. Boom!"),
    Malik("Malik", "There's only one direction to go from here...", 2, 3, 1, CardClass.MAGE, "The unit to his left does not take the next instance of damage."),
    Brap("Brap", "Brap brap, hit 'em with the one-two!", 3, 12, 2, CardClass.BRAWLER, "Brap's quick attacks make him attack an extra time."),
    Cablooey("Cablooey", "Oh you're about to feel it now...", 3, 7, 1, CardClass.ARCHER, "Cablooey shoots the opposing unit for half of its current HP."),
    Catapulty("Catapulty", "Swing and a... heh, I never miss.", 3, 3, 5, CardClass.ARCHER, "Catapulty returns the favor by shooting the opposing unit for its own attack value."),
    Nomnom("Nomnom", "FREE FOOD?!", 3, 1, 3, CardClass.MAGE, "Nomnom's unceasing hunger grants the unit to his left life steal for the duration of the turn. Life steal heals the unit for the amount of damage it deals."),
    TimeLord("Time Lord", "Time's running out, fella. [smirk]", 3, 4, 3, CardClass.MAGE, "Time Lord warps time and space to destroy the opposing unit if both him and the opposing unit are alive by the next turn. Time's up!"),
    BigShot("Big Shot", "Now's your chance to be a [[BIG SHOT]]!", 4, 10, 1, CardClass.ARCHER, "Big Shot shoots the [[OPPOSING UNIT]] for the combined attack of all [[FRIENDLY UNITS]] on the board. [[DELICIOUS]]"),
    IceCube("Ice Cube", "Get iced, dummy.", 4, 3, 1, CardClass.MAGE, "The opposing unit cannot attack or use its effect for the next turn. No more Mr. Nice Cube."),
    Cheerleader("Cheerleader", "\"Her love, the type that makes you dedicate your life.\" ~ Unknown Musician", 4, 5, 5, CardClass.MAGE, "Cheerleader gives all friendly units on the board +3 attack and +3 HP for the duration of the turn. Go team!"),
    HungryAssassin("Hungry Assassin", "You look... delicious.", 4, 10, 10, CardClass.RARE, "Hungry Assassin sacrifices as much HP as the opposing unit's HP to destroy it. Bon appétit!"),
    Flea("Flea", "Life is too short to learn German.", 4, 1, 1, CardClass.RARE, "If Flea attacks another unit, destroy it after battle. Auf Wiedersehen!"),
    BigGunga("Big Gunga", "A sophisticated gentleman such as myself is not to be trifled with.", 5, 15, 10, CardClass.BRAWLER, "Big Gunga attacks the opposing unit. If the opposing unit dies from this attack, Big Gunga gains half its stats. Call it a gentleman's quarrel."),
    Sender("Sender", "I send you my regards.", 5, 4, 4, CardClass.ARCHER, "Sender, the divine messenger, shoots the opposing unit for the combined attack and HP values of the unit to his left. Aaaaand send!"),
    RoyalSummoner("Royal Summoner", "I summon thee!", 5, 6, 7, CardClass.MAGE, "Summon a random unit from the discard pile, deck, or hand, and place it to the right of this unit. The Royal Summoner beckons thee."),
    Copycat("Copycat", "I am thou, thou art I.", 5, 2, 2, CardClass.RARE, "For every unit on the board, gain 1 HP and 1 Attack for the duration of the turn. The Copycat is you, and you are the Copycat."),
    UnceasingVoid("The Unceasing Void", "Infinity.", 5, 30, 0, CardClass.RARE, "While The Unceasing Void is on the board, you cannot die. Infinity is a long time.")
]