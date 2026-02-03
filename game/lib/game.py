# Copyright 2019 Amanda Justiniano amjustin@bu.edu

"""
Core game engine framework for the Digital Card Deck System.

This module provides the base classes and functionality for implementing
card games with RFID-enabled e-paper cards.
"""

import sys
import logging

from time import sleep
from .deck import CardDeck
from .rfid_info import get_card
from .send_info import writeData


class GameFailure(Exception):
    """Base exception for game-related errors."""

class Hand:
    """Represents a player's hand of cards."""
    
    def __init__(self, cards):
        """Initialize a player's hand with specified cards.

        Args:
            cards (list): List of Card objects belonging to the hand.
        """
        self.cards = cards
        self.active = cards  # Cards available to play
        self.dead = []       # Cards that have been played/discarded
        self.rfids = []      # RFID identifiers for physical cards
        self.turn = None     # Whether it's this player's turn

    def place(self, card):
        """Place a card into play and remove it from active hand.

        Args:
            card: Card object to place in play.

        Returns:
            The card that was placed.
        """
        temp = card
        self.active.remove(card)
        return temp

    def collect(self, cards):
        """Collect cards that belong to this hand (e.g., won cards).

        Args:
            cards (list): List of Card objects to add to the hand.
        """
        for card in cards:
            self.dead.append(card)

    def register(self, req_hw):
        """Register physical RFID cards for this hand.

        Args:
            req_hw (int): Number of physical cards required.
        """
        try:
            while len(self.rfids) < req_hw:
                self.rfids.append(get_card())
        except Exception as err:
            print(f"Error registering RFID cards: {err}")


class Game:
    """Base class for all card games in the Digital Card Deck System.
    
    This class provides the core framework for game management, including
    card distribution, player hand management, RFID integration, and
    game state tracking.
    """
    
    def __init__(self, name, req_hw, deck_type="standard", players=2):
        """Initialize a game instance.

        Args:
            name (str): Name of the game.
            req_hw (int): Number of required physical cards per player.
            deck_type (str): Type of deck to use (e.g., "standard", "spanish").
                Defaults to "standard".
            players (int): Number of players. Defaults to 2.
        """
        self.name = name
        self.deck = CardDeck(name=deck_type)
        self.graveyard = []  # Discarded/played cards
        self.hands = {}      # Player hands dictionary
        self.players = players
        self.req_hw = req_hw  # Required hardware cards per player
        self.log = logging.getLogger()
        self.log.level = logging.DEBUG

    def is_hw_registered(self):
        """Check if all physical cards have been registered.

        Returns:
            bool: True if all players have registered their cards, False otherwise.
        """
        if self.hands:
            count = 0
            for hand in self.hands.values():
                if hand.rfids:
                    count += 1
            if count == len(self.hands):
                return True
        return False

    def is_turn(self, player_hw):
        """Check if it is the player's turn based on RFID value.

        Args:
            player_hw: RFID identifier of the card.

        Returns:
            bool: True if it's the player's turn, False otherwise.
        """
        player = self.get_player(player_hw)
        return self.hands[player].turn is True

    def get_player(self, player_hw):
        """Get player ID from the provided RFID value.

        Args:
            player_hw: RFID identifier of the card.

        Returns:
            int: Player ID (0-indexed).

        Raises:
            GameFailure: If no player is found for the given RFID.
        """
        for player in range(self.players):
            if player_hw in self.hands[player].rfids:
                return player
        
        raise GameFailure(f"Player not found for RFID: {player_hw}")

    def get_hw(self):
        """Read RFID card from hardware.

        Returns:
            int: RFID identifier of the scanned card.
        """
        return get_card()

    def send_info(self, info):
        """Send information to the e-paper display hardware.

        Args:
            info (str): Information to display on the card.

        Returns:
            int: Status code from write operation.
        """
        return writeData(info)

    def init(self):
        """Initialize the game, set up hardware cards and virtual deck."""
        print(f"Welcome to {self.name}!")
        try:
            self.create_hands()
        except Exception as err:
            print(f"Error dealing cards: {err}")

    def discard(self, cards):
        """Place cards in the graveyard (discard pile).

        Args:
            cards (list): List of Card objects to be discarded.
        """
        try:
            for card in cards:
                self.graveyard.append(card)
        except Exception as err:
            print(f"Error discarding cards {cards}: {err}")

    def create_hands(self):
        """Create hands for all players.
        
        This method should be overridden by each individual game implementation
        to define how cards are distributed to players.
        """
        pass

    def start(self):
        """Start the game and begin gameplay loop.
        
        This method should be overridden by each individual game implementation
        to define the game's main logic and flow.
        """
        pass

    def save(self, game_name):
        """Save the current game state.

        Args:
            game_name (str): Name/identifier for the saved game.
            
        Note:
            This method should be overridden to implement actual save functionality.
        """
        pass

    def load(self):
        """Load a previously saved game state.
        
        This will restore all player hands, game score, and game state.
        
        Note:
            This method should be overridden to implement actual load functionality.
        """
        pass

    def update(self):
        """Update the game score according to game-specific rules.
        
        This method should be overridden by each game implementation to
        define how scoring works for that particular game.
        """
        pass
