# 🔥 TermEmoji - IMMORTAL COOL PRO Battle Royale

An epic terminal-based emoji battle royale game with modular architecture, infinite respawns, power-ups, and advanced AI!

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

## 🎯 Controls

- **A/D**: Move left/right
- **W**: Jump
- **S**: Attack
- **F**: Special ability (multi-shot)
- **Q**: Quit

## 💎 Power-ups

- **❤️ Health**: Restore 50 HP
- **⚡ Speed**: 50% speed boost for 10 seconds
- **💥 Damage**: 80% damage boost for 8 seconds
- **🛡️ Shield**: Absorbs 50% damage for 5 seconds
- **♾️ Infinite**: Complete immortality for 15 seconds

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
└── README.md       # This file
```

### 🔧 Module Responsibilities

#### `main.py`
- Game initialization and main loop
- Input handling
- Orchestrates all other modules

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

## 🚀 Installation & Running

### Prerequisites
- Python 3.7+
- Terminal with curses support

### On Windows
```bash
pip install windows-curses
```

### Running the Game
```bash
python main.py
```

## 🎮 Gameplay

1. **Start**: You spawn as 😎 with 5 AI opponents
2. **Fight**: Use A/D to move, W to jump, S to attack
3. **Power-ups**: Collect power-ups for temporary buffs
4. **Special**: Press F for multi-shot special ability
5. **Survive**: Respawn infinitely and build combos!

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

## 📄 License

This project is open source and available under the MIT License.

---

**Enjoy the IMMORTAL COOL PRO battle royale experience!** 🔥⚡💥
