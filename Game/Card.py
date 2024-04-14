from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Optional

class CardClass(Enum):
    BRAWLER = auto()
    ARCHER = auto()
    MAGE = auto()
    RARE = auto()

class CardColor(Enum):
    BLUE = auto()
    GREEN = auto()
    ORANGE = auto()
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
        
        self.name = name
        self.description = description
        self.tier = tier
        self.hp = hp
        self.attack = attack
        self.card_class = CardClass(card_class)
        self.color = CardColor(list(CardColor)[tier-1])
        self.effect_description = effect_description

    @abstractmethod
    def activate_effect(self):
        """Method to activate the card's special effect"""
        pass

    def perform_attack(self, target):
        """Method to perform an attack on a target"""
        target.hp -= self.attack
        print(f"{self.name} attacks {target.name} for {self.attack} damage!")

    def die(self):
        """Method to handle the card's death"""
        print(f"{self.name} has died.")

    def get_card_info(self):
        return (
            f"-=| Card Information| =-\n"
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
    def activate_effect(self):
        """This card has no special effect."""
        pass

# Specific card implementations for special effects
class Grag(Card):
    def activate_effect(self):
        print(f"Add 2 health to the unit to the left")
        # todo: implement effect

class Pew(Card):
    def activate_effect(self):
        print(f"Deal 2 damage to the unit in front of it")
        # todo: implement effect

class Rasmus(Card):
    def activate_effect(self):
        print(f"Make the unit to the left attack again")
        # todo: implement effect

class Bank(Card):
    def activate_effect(self):
        print(f"If a friendly unit dies, Bank gains 1 attack and 1 HP")

class PewPew(Card):
    def activate_effect(self):
        print(f"Deal 2 damage to a unit")

class Boom(Card):
    def activate_effect(self):
        print(f"Shoot opposing unit for 1 damage for each friendly unit on the board")

class Malik(Card):
    def activate_effect(self):
        print(f"Unit to the left does not take the next instance of damage")

class Brap(Card):
    def activate_effect(self):
        print(f"Attack the opposing unit.") # (Extra attack since this happens during effect activation phase)

class Cablooey(Card):
    def activate_effect(self):
        print(f"Shoot opposing unit for 50% of its HP.")

class Catapulty(Card):
    def activate_effect(self):
        print(f"Shoot the opposing unit for its own attack value.")

class Nomnom(Card):
    def activate_effect(self):
        print(f"Unit to the left gains life steal for the duration of the turn. Life steal heals the unit for the amount of damage it deals.")

class TimeLord(Card):
    def activate_effect(self):
        print(f"If both this unit and the opposing unit are alive by the next turn, destroy the opposing unit.")

class BigShot(Card):
    def activate_effect(self):
        print(f"Shoot opposing unit for the combined attack of all friendly units on the board.")

class IceCube(Card):
    def activate_effect(self):
        print(f"Freeze the opposing unit for the next turn.")

class Cheerleader(Card):
    def activate_effect(self):
        print(f"Give all friendly units on the board +3 attack and +3 HP for the duration of the turn.")

class HungryAssassin(Card):
    def activate_effect(self):
        print(f"Sacrifice as much HP as the opposing unit's HP to destroy it.")

class Flea(Card):
    def activate_effect(self):
        print(f"If this unit attacks another unit, destroy it after battle.")

class BigGunga(Card):
    def activate_effect(self):
        print(f"This unit attacks the opposing unit. If the opposing unit dies from this attack, gain half its stats.")

class Sender(Card):
    def activate_effect(self):
        print(f"Add to Sender's attack stat the attack stat of the unit to its left.")

class RoyalSummoner(Card):
    def activate_effect(self):
        print(f"Summon a random unit from the discard pile, deck, or hand, and place it to the right of this unit.")

class Copycat(Card):
    def activate_effect(self):
        print(f"When a friendly unit activates its ability, gain 2 attack and 2 HP permanently.") # Permanently means for the duration of the match, not like forever

class UnceasingVoid(Card):
    def activate_effect(self):
        print(f"If this unit is on the board, you cannot die.")


# List of all cards
cards_list = [
    SimpleCard("Greg", "Ooga booga", 1, 1, 5, CardClass.BRAWLER),
    SimpleCard("Grog", "Unga bunga", 1, 4, 2, CardClass.BRAWLER),
    Grag("Grag", "Gonk gonk", 1, 1, 2, CardClass.BRAWLER, "Heals the unit to his left by 2 HP out of the kindness of his heart"),
    Pew("Pew", "I am an archer. I go pew. Just once.", 1, 1, 1, CardClass.ARCHER, "Deals 2 damage to the unit in front of him. Pew!"),
    Rasmus("Rasmus", "I am Rasmus the Almighty. Tremble before me.", 1, 2, 2, CardClass.MAGE, "Inspires the unit to his left to attack twice."),
    SimpleCard("Bonk", "Bonk bonk", 2, 5, 6, CardClass.BRAWLER),
    Bank("Bank", "Cha-ching!", 2, 3, 3, CardClass.BRAWLER, "If a friendly unit dies, gain 1 mana"),
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
    Sender("Sender", "I send you my regards.", 5, 4, 4, CardClass.ARCHER, "Add to Sender's attack stat the attack stat of the unit to his left. Regards, Sender."),
    RoyalSummoner("Royal Summoner", "I summon thee!", 5, 6, 7, CardClass.MAGE, "Summon a random unit from the discard pile, deck, or hand, and place it to the right of this unit. The Royal Summoner beckons thee."),
    Copycat("Copycat", "I am thou, thou art I.", 5, 2, 2, CardClass.RARE, "When a friendly unit activates its ability, gain 2 attack and 2 HP permanently. The Copycat is you, and you are the Copycat."),
    UnceasingVoid("The Unceasing Void", "Infinity.", 5, 30, 0, CardClass.RARE, "If the Unceasing Void is on the board, you cannot die. Infinity is a long time.")
]

def print_cards():
    for card in cards_list:
        print(card.get_card_info())
        print()

# Debugging
# print_cards()