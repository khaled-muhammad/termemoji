# 🔥 TermEmoji - IMMORTAL COOL PRO Battle Royale

An epic terminal-based emoji battle royale game with modular architecture, infinite respawns, power-ups, advanced AI, and multiplayer support!

## 📦 Installation

### Quick Install

#### Windows
1. Download the latest release from [GitHub Releases](https://github.com/yourusername/termemoji/releases)
2. Extract the archive
3. Double-click `install-windows.bat` or run:
   ```cmd
   python -m pip install -e .
   ```

#### macOS/Linux
1. Download the latest release from [GitHub Releases](https://github.com/yourusername/termemoji/releases)
2. Extract the archive
3. Run:
   ```bash
   chmod +x install-unix.sh && ./install-unix.sh
   ```
   Or manually:
   ```bash
   python3 -m pip install -e .
   ```

### From Source

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/termemoji.git
   cd termemoji
   ```

2. Install the game:
   ```bash
   python -m pip install -e .
   ```

3. Run the game:
   ```bash
   python main.py
   ```

### Using Make (Linux/macOS)

```bash
make install    # Install the package
make run        # Run the game
make run-server # Run the server
make help       # Show all available commands
```

## 🚀 Features

### 🔥 IMMORTAL FEATURES
- **Infinite Respawns**: Players respawn after 3 seconds when defeated
- **Infinite Mode Power-up**: Complete immortality for 15 seconds
- **Invulnerability**: 2-second invulnerability after respawning
- **Health Power-ups**: Restore 50 HP instantly

### 🎮 COOL FEATURES
- **Visual Effects**: Particle explosions, projectile trails, animated effects
- **Color Support**: Colored messages and enhanced visuals
- **Special Abilities**: Multi-shot special attacks
- **Combo System**: Chain attacks for combo multipliers
- **Power-ups**: 5 different types with unique effects
- **Advanced AI**: Smart enemies with personality and special abilities

### ⚡ PRO FEATURES
- **Enhanced Combat**: Damage multipliers, shields, knockback physics
- **Statistics Tracking**: Kills, deaths, combos, game time
- **Advanced AI**: Enemies use special abilities and have different personalities
- **Smooth Gameplay**: 30 FPS with better physics
- **Dynamic Power-ups**: Spawn randomly and provide temporary buffs

### 🌐 MULTIPLAYER FEATURES
- **Real-time Multiplayer**: Battle against other players online
- **Lobby System**: Join rooms, see player list, ready states
- **Game Start Countdown**: Automatic countdown when all players are ready
- **Synchronized Combat**: Real-time position and attack synchronization
- **Room-based Matchmaking**: Create or join specific game rooms

## 🎯 Controls

### Singleplayer
- **A/D**: Move left/right
- **W**: Jump
- **S**: Attack
- **F**: Special ability (multi-shot)
- **Q**: Quit

### Multiplayer Lobby
- **R**: Toggle ready state
- **Q**: Quit lobby

## 💎 Power-ups

- **❤️ Health**: Restore 50 HP
- **⚡ Speed**: 50% speed boost for 10 seconds
- **💥 Damage**: 80% damage boost for 8 seconds
- **🛡️ Shield**: Absorbs 50% damage for 5 seconds
- **♾️ Infinite**: Complete immortality for 15 seconds

## 🚀 Quick Start

### Single Player
```bash
python main.py
# Select option 1 for single player
```

### Multiplayer
1. Start the server:
   ```bash
   python server.py --host 0.0.0.0 --port 8765
   ```

2. Start the game:
   ```bash
   python main.py
   # Select option 2 or 3 for multiplayer
   ```

## 🏗️ Modular Architecture

The game is built with a clean, modular architecture:

### 📁 File Structure

```
termemoji/
├── main.py          # Main game entry point
├── utils.py         # Utilities, constants, and helper functions
├── models.py        # Game entity classes (Entity, Projectile, PowerUp, Particle)
├── ai.py           # AI behavior and logic
├── renderer.py     # Rendering and UI components
├── game_logic.py   # Game mechanics and physics
├── server.py       # Multiplayer server with lobby system
├── net_client.py   # Network client for multiplayer
├── lobby_screen.py # Lobby UI and management
└── README.md       # This file
```

### 🔧 Module Responsibilities

#### `main.py`
- Game initialization and main loop
- Input handling
- Orchestrates all other modules
- Multiplayer game flow

#### `utils.py`
- Game constants (FPS, gravity, controls)
- Power-up definitions
- Helper functions (distance, particle creation)
- Color setup

#### `models.py`
- **Entity**: Base class for all game characters
- **Projectile**: Attack projectiles with trails
- **PowerUp**: Collectible power-up items
- **Particle**: Visual effect particles

#### `ai.py`
- **AIController**: Handles AI behavior
- AI movement, attacking, and special abilities
- AI entity creation with personalities

#### `renderer.py`
- **Renderer**: Handles all visual rendering
- UI components and HUD
- Particle and effect rendering
- Color support

#### `game_logic.py`
- **GameLogic**: Core game mechanics
- Physics updates
- Collision detection
- Power-up collection
- Message management

#### `server.py`
- **Multiplayer Server**: TCP socket server
- **Room Management**: Create and manage game rooms
- **Lobby System**: Handle ready states and countdown
- **Client Synchronization**: Relay game state between players

#### `net_client.py`
- **Network Client**: TCP client for multiplayer
- **Message Handling**: Send/receive game messages
- **Connection Management**: Handle server connections

#### `lobby_screen.py`
- **Lobby UI**: Player list and ready states
- **Countdown Display**: Game start countdown
- **Input Handling**: Ready toggle and lobby controls

## 🚀 Installation & Running

### Prerequisites
- Python 3.8+
- Terminal with curses support

### Windows Requirements
Windows requires the `windows-curses` package for terminal support:

```bash
pip install windows-curses
```

Or install automatically with the game:
```bash
pip install -e .
```

### Running the Game

#### Singleplayer
```bash
python main.py
# Select "1) Singleplayer" from the menu
```

#### Multiplayer
```bash
# Start the server first
python server.py --host 0.0.0.0 --port 8765

# Then start clients in separate terminals
python main.py
# Select "2) Multiplayer: Join Room" or "3) Multiplayer: Create Room"
```

## 🎮 Gameplay

### Singleplayer
1. **Start**: You spawn as 😎 with 2 AI opponents
2. **Fight**: Use A/D to move, W to jump, S to attack
3. **Power-ups**: Collect power-ups for temporary buffs
4. **Special**: Press F for multi-shot special ability
5. **Survive**: Respawn infinitely and build combos!

### Multiplayer
1. **Join Lobby**: Connect to server and join a room
2. **Ready Up**: Press R to toggle ready state
3. **Wait for Players**: Need at least 2 players ready
4. **Countdown**: 5-second countdown when all ready
5. **Battle**: Fight other players in real-time!

## 🔧 Development

### Adding New Features

#### New Power-up Type
1. Add to `POWERUP_TYPES` in `utils.py`
2. Implement effect in `PowerUp.collect()` in `models.py`
3. Add visual feedback in `renderer.py`

#### New AI Behavior
1. Extend `AIController` in `ai.py`
2. Add new methods for specific behaviors
3. Update `update_ai_entity()` to use new logic

#### New Visual Effects
1. Create new particle types in `models.py`
2. Add rendering logic in `renderer.py`
3. Integrate with `game_logic.py`

### Code Style
- Follow PEP 8
- Use docstrings for all functions
- Keep modules focused on single responsibility
- Use type hints where helpful

## 🎯 Future Enhancements

- [ ] Multiple game modes
- [ ] Save/load high scores
- [ ] Custom character selection
- [ ] Network multiplayer
- [ ] Sound effects
- [ ] More power-up types
- [ ] Level progression system

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📦 Releases

### Latest Release
Download the latest release from [GitHub Releases](https://github.com/yourusername/termemoji/releases)

### Release Assets
- **Windows**: `termemoji-v1.0.0-windows.zip` - Windows installer and scripts
- **macOS**: `termemoji-v1.0.0-macos.tar.gz` - macOS installer and scripts  
- **Linux**: `termemoji-v1.0.0-linux.tar.gz` - Linux installer and scripts
- **Source**: `termemoji-1.0.0.tar.gz` - Source distribution

### Building Releases
```bash
# Build release packages
python build_release.py

# Or use make
make release
```

## 🔧 Development

### Prerequisites
- Python 3.8+
- Terminal with curses support
- **Windows**: `windows-curses` package (installed automatically)

### Setup Development Environment
```bash
# Install in development mode
make install

# Run tests
make test

# Build package
make build

# Clean build artifacts
make clean
```

### Adding New Features

#### New Power-up Type
1. Add to `POWERUP_TYPES` in `utils.py`
2. Implement effect in `PowerUp.collect()` in `models.py`
3. Add visual feedback in `renderer.py`

#### New AI Behavior
1. Extend `AIController` in `ai.py`
2. Add new methods for specific behaviors
3. Update `update_ai_entity()` to use new logic

#### New Visual Effects
1. Create new particle types in `models.py`
2. Add rendering logic in `renderer.py`
3. Integrate with `game_logic.py`

### Code Style
- Follow PEP 8
- Use docstrings for all functions
- Keep modules focused on single responsibility
- Use type hints where helpful

## 🎯 Future Enhancements

- [x] Custom character selection ✅
- [x] Network multiplayer ✅
- [x] Lobby system ✅
- [ ] Multiple game modes
- [ ] Save/load high scores
- [ ] Sound effects
- [ ] More power-up types
- [ ] Level progression system

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

**Enjoy the IMMORTAL COOL PRO battle royale experience!** 🔥⚡💥
