# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Custom character selection system with 8 unique characters
- Character stats system (HP, Speed, Damage multipliers)
- ASCII fallback support for terminals that don't support emojis
- Improved character selection screen with better stability
- GitHub Actions workflows for automated testing and releases
- Cross-platform build system
- Professional packaging setup

### Changed
- Updated character emojis for better compatibility
- Improved screen clearing in character selection
- Enhanced multiplayer synchronization
- Better error handling across all platforms

### Fixed
- Screen clearing issues in character selection
- Multiplayer respawn synchronization
- Remote player animation and invulnerability timers
- Terminal compatibility issues

## [1.0.0] - 2024-01-XX

### Added
- Terminal-based emoji battle royale game
- Single-player mode with AI opponents
- Multiplayer mode with lobby system
- Real-time multiplayer combat
- 8 unique characters with different stats
- Power-up system (health, speed, damage, shield, infinite mode)
- Particle effects and visual feedback
- Combo system
- Special abilities for each character
- Lobby system with ready states and countdown
- Deterministic spawn positioning
- Cross-platform support (Windows, macOS, Linux)

### Features
- **Game Modes**: Single-player, Multiplayer (Join/Create Room)
- **Characters**: Warrior, Ninja, Tank, Mage, Archer, Berserker, Monk, Robot
- **Controls**: A/D (move), W (jump), S (attack), F (special), Q (quit)
- **Multiplayer**: Real-time combat, lobby system, synchronized respawns
- **Visual Effects**: Particle systems, projectile trails, invulnerability effects
- **AI**: Smart opponents with different behaviors and strategies

### Technical
- Built with Python curses library
- TCP socket networking for multiplayer
- Modular architecture (main.py, models.py, ai.py, renderer.py, game_logic.py)
- No external dependencies (pure Python standard library)
- Cross-platform terminal support
