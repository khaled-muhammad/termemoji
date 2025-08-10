# 🔥 TermEmoji - IMMORTAL COOL PRO Battle Royale

An epic terminal-based emoji battle royale game with modular architecture, infinite respawns, power-ups, advanced AI, and multiplayer support!

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

## 📦 Installation & Build

### 🚀 Quick Start (Pre-built Binaries)

1. Go to the [Releases](https://github.com/yourusername/termemoji/releases) page
2. Download the appropriate binary for your platform:
   - `termemoji-linux-x64.zip` for Linux
   - `termemoji-windows-x64.zip` for Windows
   - `termemoji-macos-x64.zip` for macOS
3. Extract the archive
4. Run the game:
   - **Linux/macOS**: `./run-game.sh` or `./termemoji`
   - **Windows**: `run-game.bat` or `termemoji.exe`

### 🔧 Build from Source

1. Clone the repository:
```bash
git clone https://github.com/yourusername/termemoji.git
cd termemoji
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Build the binaries:
```bash
python build.py
```

4. Run the game:
```bash
python main.py
```

### 🏗️ Modular Architecture

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
- Python 3.7+
- Terminal with curses support

### On Windows
```bash
pip install windows-curses
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

## 🚀 Creating Releases

### Automated Releases (GitHub Actions)

1. Create and push a tag:
```bash
git tag v1.0.0
git push origin v1.0.0
```

2. GitHub Actions will automatically:
   - Build binaries for all platforms
   - Create a GitHub release
   - Upload the binaries as release assets

### Manual Releases

1. Build for all platforms:
```bash
python release.py v1.0.0
```

2. Or build only:
```bash
python release.py v1.0.0 --build-only
```

3. Or create release only:
```bash
python release.py v1.0.0 --release-only
```

### Build Scripts

- `build.py`: Build game and server binaries
- `release.py`: Create GitHub releases
- `.github/workflows/build.yml`: Automated CI/CD

## 🎯 Future Enhancements

- [x] Custom character selection
- [x] Network multiplayer
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

This project is open source and available under the MIT License.

---

**Enjoy the IMMORTAL COOL PRO battle royale experience!** 🔥⚡💥
