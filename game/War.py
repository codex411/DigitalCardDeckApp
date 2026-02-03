# Copyright 2019 Amanda Justiniano amjustin@bu.edu

"""
War card game implementation for the Digital Card Deck System.

War is a simple card game where players battle with cards of equal rank.
The player with the higher card wins both cards. In case of a tie, a "war"
is declared with additional cards.

Game Rules Reference:
https://bicyclecards.com/how-to-play/war/

THE DEAL:
The deck is divided evenly, with each player receiving 26 cards,
dealt one at a time, face down.

THE PLAY:
Each player turns up a card at the same time and the player with
the higher card takes both cards and puts them, face down, on the
bottom of their stack.

If the cards are the same rank, it is War. Each player turns up
one card face down and one card face up. The player with the higher
cards takes both piles (six cards). If the turned-up cards are again
the same rank, each player places another card face down and turns
another card face up. The player with the higher card takes all 10
cards, and so on.

HOW TO KEEP SCORE:
The game ends when one player has won all the cards.
"""

import logging
import time

from game.lib.game import Game, Hand, GameFailure

class War(Game):
    """War card game implementation."""
    
    def __init__(self):
        """Initialize a War game instance."""
        super(War, self).__init__("War", 2)
        self.in_play = []  # Cards currently in play for the round

    def switch_turns(self):
        """Simple method to switch turns for the players."""
        for player in range(self.players):
            self.hands[player].turn = not self.hands[player].turn

    def check_winner(self, current_round):
        """Determine the winner of the current round or declare a war.

        Args:
            current_round (list): List of dictionaries containing player cards.

        Returns:
            int: Player ID of the winner, or -1 if it's a tie (war).
        """
        winner = None
        translate_A_K = {'A': 'Z', 'K': 'X'}  # Translate A and K for comparison

        # Get first player's card value
        card_value1 = current_round[0][0].value
        if card_value1 in translate_A_K.keys():
            card_value1 = translate_A_K[card_value1]

        # Get second player's card value
        card_value2 = current_round[1][1].value
        if card_value2 in translate_A_K.keys():
            card_value2 = translate_A_K[card_value2]

        # Compare card values
        if card_value1 > card_value2:
            winner = list(current_round[0].keys())
        elif card_value2 > card_value1:
            winner = list(current_round[1].keys())
        elif card_value1 == card_value2:
            print("We have a tie! War declared!")
            return -1

        print(f"Player {winner} won this round!")
        return winner[-1]

    def distribute(self, winner, current_round):
        """Distribute cards to players based on round outcome.

        Args:
            winner (int): Player ID of the winner, or -1 for a tie.
            current_round (list): List of dictionaries containing player cards.
        """
        if winner != -1:
            # Winner collects both cards
            self.hands[winner].dead.append(current_round[0][0])
            self.hands[winner].dead.append(current_round[1][1])

        # If there was a tie, return cards to active hands
        self.hands[0].active.append(current_round[0][0])
        self.hands[1].active.append(current_round[1][1])


    def create_hands(self):
        """Create and distribute hands to all players."""
        print("Creating hands and distributing cards...")
        
        # Shuffle the deck
        self.deck.shuffle()

        # Split the deck evenly between players
        deck_half = len(self.deck.cards) // self.players
        deck_halves = [
            self.deck.cards[:deck_half],
            self.deck.cards[deck_half:]
        ]
        
        for player in range(self.players):
            self.hands[player] = Hand(deck_halves[player])
            # Register physical RFID cards (2 cards per player for War)
            self.hands[player].register(self.req_hw // self.players)
            print(f"Player {player} registered RFID: {self.hands[player].rfids[-1]}")

        # Set the first player's turn to True
        self.hands[0].turn = True
        print("All players registered and ready!")

    def get_player_info(self):
        """Get card from player and display it on e-paper.

        Returns:
            dict: Dictionary mapping player ID to the card they played.
        """
        current = {}
        
        # Wait for the correct player to place their card
        while True:
            player_hw = self.get_hw()
            if self.is_turn(player_hw):
                break
            print("It's not your turn!")

        # Get the top card from the player's active hand
        player_id = self.get_player(player_hw)
        card = self.hands[player_id].active.pop(0)
        current[player_id] = card

        # Display card on e-paper
        card_info = f"{card.color} {card.value} {card.suit}"
        print(f"Playing card: {card_info}")
        self.send_info(card_info)
        time.sleep(15)  # Allow time for display update

        self.switch_turns()

        return current

    def start(self):
        """Start the War game and run the main gameplay loop.

        Returns:
            bool: True when game completes.
        """
        print("Cards are dealt. Let's start playing!")
        
        # Continue until one player has all 52 cards
        while len(self.hands[0].dead) < 52 and len(self.hands[1].dead) < 52:
            curr_round = []

            # Get cards from both players
            for player in range(self.players):
                print(f"Player {player}: Please place a card")
                curr_round.append(self.get_player_info())

            # Determine round winner
            winner = self.check_winner(curr_round)

            # Distribute cards based on outcome
            self.distribute(winner, curr_round)

            # Display current hand sizes
            for player in range(self.players):
                print(f"Player {player} has {len(self.hands[player].active)} cards remaining")

        # Announce winner
        for player in range(self.players):
            if len(self.hands[player].dead) >= 52:
                print(f"Player {player} wins!!")
                break

        return True
