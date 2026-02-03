"""
E-paper display communication interface.

This module provides functions to send card information to the Arduino
controller via I2C bus, which then updates the e-paper displays.
"""

import smbus

# Initialize I2C bus (bus 1 for Raspberry Pi)
bus = smbus.SMBus(1)

# I2C address configured in Arduino program
ARDUINO_ADDRESS = 0x04


def _string_to_bytes(value):
    """Convert a string to a list of byte values.

    Args:
        value (str): String to convert.

    Returns:
        list: List of integer byte values.
    """
    return [ord(c) for c in value]


def writeData(value):
    """Send card information to Arduino via I2C.

    Args:
        value (str): Card information string to display (e.g., "Red A Hearts").

    Returns:
        int: Status code (-1 indicates completion).
    """
    print(f"Writing to display: {value}")
    byte_value = _string_to_bytes(value)
    bus.write_i2c_block_data(ARDUINO_ADDRESS, 0x00, byte_value)
    return -1


def readData():
    """Read data from Arduino via I2C.

    Returns:
        int: Byte value read from Arduino.
    """
    data = bus.read_byte(ARDUINO_ADDRESS)
    return data
