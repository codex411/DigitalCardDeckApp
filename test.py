"""
Simple test script for the Digital Card Deck System.

This script initializes and runs a game of War for testing purposes.
"""

from game.War import War


def main():
    """Run a test game of War."""
    # Create game instance
    game = War()

    # Initialize game (deal cards, register RFID cards)
    game.init()

    # Start gameplay
    game.start()


if __name__ == '__main__':
    main()
