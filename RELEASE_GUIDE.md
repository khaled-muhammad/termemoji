# 🚀 TermEmoji Release Guide

This guide explains how to create GitHub releases with pre-built binaries for all platforms.

## 📦 What Gets Built

### Game Binary (`termemoji`)
- **Singleplayer Mode**: Battle against AI opponents
- **Multiplayer Mode**: Connect to servers and battle other players
- **Character Selection**: Choose from 8 unique characters
- **All Features**: Power-ups, special abilities, visual effects

### Server Binary (`termemoji-server`)
- **Multiplayer Server**: Host games for multiple players
- **Lobby System**: Room management and player coordination
- **Game Synchronization**: Real-time state synchronization

## 🛠️ Build System

### Files Created
- `build.py`: Main build script using PyInstaller
- `release.py`: Release management script
- `.github/workflows/build.yml`: Automated CI/CD pipeline
- `requirements.txt`: Build dependencies
- `setup.py`: Package installation script

### Build Process
1. **Clean**: Remove previous build artifacts
2. **Game Build**: Create single-file game binary
3. **Server Build**: Create single-file server binary
4. **Package**: Create platform-specific release packages
5. **Scripts**: Generate run scripts for each platform

## 🎯 Creating a Release

### Method 1: Automated (Recommended)

1. **Create a Git Tag**:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **GitHub Actions Automatically**:
   - Builds for Linux, Windows, and macOS
   - Creates GitHub release
   - Uploads binaries as release assets

### Method 2: Manual Build

1. **Build Locally**:
   ```bash
   python build.py
   ```

2. **Create Release**:
   ```bash
   python release.py v1.0.0
   ```

### Method 3: Step by Step

1. **Install Dependencies**:
   ```bash
   pip install pyinstaller
   ```

2. **Build Game**:
   ```bash
   pyinstaller --onefile --name=termemoji main.py
   ```

3. **Build Server**:
   ```bash
   pyinstaller --onefile --name=termemoji-server server.py
   ```

4. **Package Release**:
   ```bash
   # Create release directory
   mkdir termemoji-release
   cp dist/termemoji* termemoji-release/
   cp README.md termemoji-release/
   
   # Create run scripts
   echo '#!/bin/bash' > termemoji-release/run-game.sh
   echo './termemoji' >> termemoji-release/run-game.sh
   chmod +x termemoji-release/run-game.sh
   
   # Create archive
   zip -r termemoji-release.zip termemoji-release/
   ```

## 📋 Release Checklist

### Before Release
- [ ] Test game functionality
- [ ] Test server functionality
- [ ] Update version numbers
- [ ] Update changelog
- [ ] Test build process

### During Release
- [ ] Create git tag
- [ ] Push tag to trigger CI/CD
- [ ] Verify GitHub Actions success
- [ ] Check release assets
- [ ] Test downloaded binaries

### After Release
- [ ] Update documentation
- [ ] Announce on social media
- [ ] Monitor for issues
- [ ] Plan next release

## 🎮 Release Assets

### Binary Files
- `termemoji`: Game executable
- `termemoji-server`: Server executable

### Run Scripts
- `run-game.sh` (Linux/macOS): Start the game
- `run-server.sh` (Linux/macOS): Start the server
- `run-game.bat` (Windows): Start the game
- `run-server.bat` (Windows): Start the server

### Documentation
- `README.md`: Game documentation and instructions

## 🔧 Platform Support

### Linux
- **Architecture**: x64
- **Dependencies**: None (static binary)
- **Terminal**: Any terminal with curses support

### Windows
- **Architecture**: x64
- **Dependencies**: None (static binary)
- **Terminal**: Windows Terminal, CMD, PowerShell

### macOS
- **Architecture**: x64, ARM64 (M1/M2)
- **Dependencies**: None (static binary)
- **Terminal**: Terminal.app, iTerm2

## 🐛 Troubleshooting

### Build Issues
- **PyInstaller not found**: `pip install pyinstaller`
- **Permission denied**: `chmod +x dist/termemoji`
- **Missing dependencies**: Check `requirements.txt`

### Runtime Issues
- **Terminal compatibility**: Use modern terminal emulator
- **Curses support**: Ensure terminal supports curses
- **Network issues**: Check firewall settings for multiplayer

### Release Issues
- **GitHub Actions failure**: Check workflow logs
- **Asset upload failure**: Verify file sizes and permissions
- **Tag issues**: Ensure proper git tag format (v1.0.0)

## 📈 Version Management

### Version Format
- **Format**: `vMAJOR.MINOR.PATCH`
- **Example**: `v1.0.0`, `v1.1.2`, `v2.0.0`

### Version Types
- **Major**: Breaking changes, new features
- **Minor**: New features, backward compatible
- **Patch**: Bug fixes, minor improvements

### Changelog
Keep a `CHANGELOG.md` file with:
- New features
- Bug fixes
- Breaking changes
- Known issues

## 🎯 Best Practices

### Before Each Release
1. **Test thoroughly** on all platforms
2. **Update documentation** with new features
3. **Check dependencies** for security updates
4. **Review code** for any last-minute fixes

### Release Process
1. **Use semantic versioning** for tags
2. **Write clear release notes** describing changes
3. **Test the release** after it's published
4. **Monitor feedback** from users

### Maintenance
1. **Keep build scripts updated** with new dependencies
2. **Monitor GitHub Actions** for build issues
3. **Update platform support** as needed
4. **Maintain backward compatibility** when possible

---

**Happy releasing! 🚀🎮**
