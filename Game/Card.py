from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Optional

class CardClass(Enum):
    BRAWLER = auto()
    ARCHER = auto()
    MAGE = auto()
    RARE = auto()

class Card(ABC):
    """A base class representing a card in the game.

    Attributes:
        name (str): The name of the card.
        description (str): The description of the card.
        tier (int): The tier of the card (1 to 5)
        mana_cost (int): The mana cost required to play the card.
        hp (int): The health points of the card.
        attack (int): The attack points of the card.
        effect_description (str, optional): The description of the card's special effect.

    Methods:
        activate_effect(): Method to activate the card's special effect.
        attack(target): Method to perform an attack on a target.
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

class SimpleCard(Card):
    def activate_effect(self):
        """This card has no special effect."""
        pass

# Specific card implementations for special effects
class Grag(Card):
    def activate_effect(self):
        print(f"Add 2 health to a unit")
        # todo: implement effect

class Pew(Card):
    def activate_effect(self):
        print(f"Deal 2 damage to a unit")
        # todo: implement effect

class Rasmus(Card):
    def activate_effect(self):
        print(f"Make a unit attack again")
        # todo: implement effect


# List of all cards
cards_list = [
    SimpleCard("Greg", "Ooga booga", 1, 1, 5, CardClass.BRAWLER),
    SimpleCard("Grog", "Unga bunga", 1, 4, 2, CardClass.BRAWLER),
    Grag("Grag", "Gonk gonk", 1, 1, 2, CardClass.BRAWLER, "Heals a selected unit by 2 HP out of the kindness of his heart"),
    Pew("Pew", "Pew pew", 1, 1, 1, CardClass.ARCHER, "Deals 2 damage to a selected unit. Pew pew pew!"),
    Rasmus("Rasmus", "I am Rasmus the Almighty. Tremble before me.", 1, 2, 2, CardClass.MAGE, "Makes a selected unit attack again by inspiring them with his greatness")
]

for card in cards_list:
    print(f"Name: {card.name}")
    print(f"Description: {card.description}")
    print(f"Tier: {card.tier}")
    print(f"HP: {card.hp}")
    print(f"Attack: {card.attack}")
    print(f"Card Class: {card.card_class.name}")
    print(f"Effect Description: {card.effect_description}")
    print()