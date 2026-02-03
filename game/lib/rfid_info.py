"""
RFID card reader interface for the Digital Card Deck System.

This module handles communication with the MFRC522 RFID reader to
identify physical cards placed in the card port.
"""

from time import sleep
import sys

from mfrc522 import SimpleMFRC522

# Initialize RFID reader
reader = SimpleMFRC522()


def get_card():
    """Read RFID identifier from a card placed near the reader.

    Returns:
        int: RFID identifier of the scanned card.

    Raises:
        KeyboardInterrupt: If the operation is interrupted.
    """
    print("Reading RFID card...")
    id_card = None
    try:
        print("Hold a tag near the reader")
        id, text = reader.read()
        sleep(5)
        id_card = id
    except KeyboardInterrupt:
        # GPIO cleanup would be needed if GPIO was imported
        raise
    return id_card
