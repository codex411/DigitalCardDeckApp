# Digital Card Deck System

A modern e-paper based playing card system that enables multiple card games using a single digital deck. This project combines RFID technology, e-paper displays, and a Python game engine to create an interactive card gaming experience.

## 🎯 Overview

The Digital Card Deck System transforms traditional card games into a digital experience. Players use physical e-paper cards that can dynamically display different card values, controlled by a central game management system. The system supports multiple card games and can handle up to four players.

## ✨ Features

- **Multi-Game Support**: Play different card games with the same physical deck
- **E-Paper Display**: Low-power, paper-like display technology for authentic card feel
- **RFID Integration**: Automatic card identification and tracking
- **Game Management**: Central controller handles shuffling, dealing, scoring, and game rules
- **Player Support**: Designed for 2-4 players
- **Game State Management**: Save and resume game progress

## 🎮 Supported Games

- **War**: Classic card battle game
- **Brisca**: Spanish card game (40-card deck)
- **Poker**: Traditional poker (52-card deck)
- **Blackjack**: Casino-style blackjack
- **Go Fish**: Family-friendly card matching game

## 🏗️ Architecture

### System Components

```
┌─────────────────┐
│  Game Engine    │  ← Manages game logic, rules, and state
├─────────────────┤
│  RFID Reader    │  ← Identifies physical cards
├─────────────────┤
│  E-Paper Driver │  ← Updates card displays
├─────────────────┤
│  GUI Interface  │  ← User interaction and game selection
└─────────────────┘
```

### Software Design

The system consists of three main components:

1. **Game Engine**: Core framework managing game rules, card distribution, scoring, and game state
2. **RFID Driver**: Handles communication between physical cards and the game engine
3. **GUI Interface**: Touch-screen interface for game selection and settings

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- Raspberry Pi (for hardware integration)
- MFRC522 RFID Reader
- E-paper displays
- Kivy (for GUI)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd digital-card-deck
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure hardware connections (see Hardware Setup section)

### Running the Application

**GUI Mode:**
```bash
python app.py
```

**Command Line Mode:**
```bash
python test.py
```

## 🎲 Game Flow

1. **Game Selection**: Choose a game from the available options
2. **Card Registration**: Place physical cards in the card port to register them
3. **Deal Cards**: System automatically deals cards to each player
4. **Gameplay**: Players place cards in the card port to refresh/play cards
5. **Score Tracking**: System automatically tracks scores and game state

## 🔧 Hardware Setup

### Raspberry Pi and RFID Wiring

The system uses MFRC522 RFID reader connected via SPI to the Raspberry Pi. See `doc/rasppi_rfid.png` for wiring diagram.

### Card Port

The card port serves as the interface between e-cards and the game controller, providing:
- Power supply for e-paper displays
- I/O interface for card updates
- RFID reading capability

## 📁 Project Structure

```
digital-card-deck/
├── app.py                 # Main GUI application
├── game/                  # Game implementations
│   ├── War.py            # War game logic
│   ├── Briscas.py        # Brisca game logic
│   └── lib/              # Core game framework
│       ├── game.py       # Base game engine
│       ├── deck.py       # Card deck management
│       ├── rfid_info.py  # RFID communication
│       └── send_info.py  # E-paper communication
├── hw/                   # Hardware integration code
│   ├── arduino/          # Arduino firmware
│   └── raspi/           # Raspberry Pi scripts
└── doc/                  # Documentation and diagrams
```

## 🎯 User Stories

- ✅ Hold at least 4 digital cards in hand
- ✅ Refresh cards without latency
- ✅ Automatic score tracking
- ✅ Game play history
- ✅ Save ongoing game state
- ✅ Switch games in under 5 seconds
- ✅ Support up to 4 players
- ✅ Intuitive game setup interface

## 🔬 Technology Stack

- **Language**: Python 3
- **GUI Framework**: Kivy
- **Hardware Communication**: 
  - MFRC522 (RFID)
  - I2C (Arduino communication)
  - SPI (RFID interface)
- **Card Definition**: YAML configuration files
- **Display Technology**: E-paper (electronic paper)

## 📊 E-Paper Technology

Electronic paper (e-paper) is the ideal display technology for this project:

- **Low Power**: Minimal power consumption, perfect for battery-powered cards
- **Flexible**: Can be integrated into card-like form factors
- **Paper-like**: Mimics the appearance of traditional playing cards
- **Persistent Display**: Maintains image without power

E-paper uses electronic ink comprised of microcapsules containing positive or negative charges. When provided with a charge, these microcapsules move through a microscopic liquid to display the card value.

## 📝 Development

### Adding a New Game

1. Create a new game class inheriting from `Game` in `game/lib/game.py`
2. Implement required methods: `create_hands()`, `start()`, `update()`
3. Add game configuration to `app.py` games dictionary
4. Create deck configuration YAML if needed

### Testing

Run the test suite:
```bash
python test.py
```

## 📄 License

Copyright 2019 Amanda Justiniano

## 🤝 Contributing

Contributions are welcome! Please ensure that:
- Core game logic remains unchanged
- New features maintain backward compatibility
- Code follows existing style conventions

## 📚 References

- [Bicycle Cards - How to Play War](https://bicyclecards.com/how-to-play/war/)
- [NH Fournier - Card Game Rules](https://www.nhfournier.es/en/como-jugar/)

---

**Note**: This project is designed for educational and prototyping purposes. Hardware setup requires Raspberry Pi and compatible RFID/e-paper hardware.
