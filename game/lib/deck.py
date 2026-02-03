# Copyright 2019 Amanda Justiniano amjustin@bu.edu

"""
Card and deck management for the Digital Card Deck System.

This module provides Card and CardDeck classes for creating and managing
playing card decks from YAML configuration files.
"""

import os
import yaml
import random


class Card:
    """Represents a single playing card."""
    
    def __init__(self, value, suit, color=None):
        """Initialize a card.

        Args:
            value: Card value (e.g., 'A', 'K', 'Q', '2', '3').
            suit: Card suit (e.g., 'Hearts', 'Spades', 'Diamonds', 'Clubs').
            color: Optional color override (e.g., 'Red', 'Black').
        """
        self.value = value
        self.suit = suit
        self.color = color


class CardDeck:
    """Manages a deck of playing cards created from YAML configuration."""
    
    def __init__(self, name="standard", namespace="game/lib/decks"):
        """Initialize a card deck from YAML configuration.

        Args:
            name (str): Name of the deck type (e.g., "standard", "spanish").
                Defaults to "standard".
            namespace (str): Directory path containing deck YAML files.
                Defaults to "game/lib/decks".
        """
        deck_path = f"{namespace}/{name}.yaml"
        with open(deck_path, 'r') as deck_file:
            deck_dict = yaml.safe_load(deck_file)
        
        self.name = deck_dict["name"]
        self.size = deck_dict["size"]
        self.suits = deck_dict["suits"]
        self.values = deck_dict["value_list"]
        self.cards = []

        # Create card objects
        self.__create_deck()

    def __create_deck(self):
        """Create all card objects for the deck based on configuration."""
        try:
            for colors in self.suits:
                for color, suits in colors.items():
                    for suit in suits:
                        for val in self.values:
                            self.cards.append(Card(val, suit, color))
        except Exception as err:
            print(f"Error creating deck {self.name}: {err}")

    def shuffle(self):
        """Shuffle the deck of cards in place."""
        try:
            random.shuffle(self.cards)
        except Exception as err:
            print(f"Error shuffling cards: {err}")
