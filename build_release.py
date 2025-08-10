#!/usr/bin/env python3
"""
Build script for TermEmoji releases
Creates distributable packages for different platforms
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running command: {cmd}")
            print(f"Error: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Exception running command {cmd}: {e}")
        return False

def create_directory(path):
    """Create directory if it doesn't exist"""
    Path(path).mkdir(parents=True, exist_ok=True)

def clean_build():
    """Clean previous build artifacts"""
    print("Cleaning previous build artifacts...")
    dirs_to_clean = ['build', 'dist', '__pycache__', '*.egg-info']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Removed {dir_name}")

def build_python_package():
    """Build Python package"""
    print("Building Python package...")
    if not run_command(f"{sys.executable} setup.py sdist bdist_wheel"):
        print("Failed to build Python package")
        return False
    print("Python package built successfully")
    return True

def create_standalone_scripts():
    """Create standalone scripts for different platforms"""
    print("Creating standalone scripts...")
    
    # Create dist directory
    create_directory("dist/scripts")
    
    # Windows batch file
    windows_script = """@echo off
python main.py %*
"""
    with open("dist/scripts/termemoji.bat", "w") as f:
        f.write(windows_script)
    
    # Windows server batch file
    windows_server_script = """@echo off
python server.py %*
"""
    with open("dist/scripts/termemoji-server.bat", "w") as f:
        f.write(windows_server_script)
    
    # Unix shell script
    unix_script = """#!/bin/bash
python3 main.py "$@"
"""
    with open("dist/scripts/termemoji.sh", "w") as f:
        f.write(unix_script)
    os.chmod("dist/scripts/termemoji.sh", 0o755)
    
    # Unix server shell script
    unix_server_script = """#!/bin/bash
python3 server.py "$@"
"""
    with open("dist/scripts/termemoji-server.sh", "w") as f:
        f.write(unix_server_script)
    os.chmod("dist/scripts/termemoji-server.sh", 0o755)
    
    print("Standalone scripts created")

def create_installer_scripts():
    """Create installer scripts for different platforms"""
    print("Creating installer scripts...")
    
    # Windows installer
    windows_installer = """@echo off
echo Installing TermEmoji...
python -m pip install --upgrade pip
python -m pip install windows-curses
python -m pip install -e .
echo Installation complete!
echo Run 'termemoji' to start the game
echo Run 'termemoji-server' to start the server
pause
"""
    with open("dist/install-windows.bat", "w") as f:
        f.write(windows_installer)
    
    # Unix installer
    unix_installer = """#!/bin/bash
echo "Installing TermEmoji..."
python3 -m pip install --upgrade pip
python3 -m pip install -e .
echo "Installation complete!"
echo "Run 'termemoji' to start the game"
echo "Run 'termemoji-server' to start the server"
"""
    with open("dist/install-unix.sh", "w") as f:
        f.write(unix_installer)
    os.chmod("dist/install-unix.sh", 0o755)
    
    print("Installer scripts created")

def create_quick_start_guide():
    """Create a quick start guide"""
    print("Creating quick start guide...")
    
    guide = """# TermEmoji Quick Start Guide

## Installation

### Windows
1. Double-click `install-windows.bat`
2. Or run: `python -m pip install -e .`

### macOS/Linux
1. Run: `chmod +x install-unix.sh && ./install-unix.sh`
2. Or run: `python3 -m pip install -e .`

## Running the Game

### Single Player
```bash
python main.py
# Then select option 1
```

### Multiplayer
1. Start the server:
   ```bash
   python server.py --host 0.0.0.0 --port 8765
   ```

2. Start the game:
   ```bash
   python main.py
   # Then select option 2 or 3
   ```

## Controls
- **A/D**: Move left/right
- **W**: Jump
- **S**: Attack
- **F**: Special ability
- **Q**: Quit

## Character Selection
Choose from 8 unique characters, each with different stats and abilities!

## System Requirements
- Python 3.8 or higher
- Terminal with curses support
  - **Windows**: Requires `windows-curses` package
  - **macOS/Linux**: Built-in curses support
- Network connection (for multiplayer)

## Troubleshooting
- **Windows**: If you get curses errors, install `windows-curses`: `pip install windows-curses`
- **Terminal Issues**: Try running in a different terminal (Windows Terminal, PowerShell, or CMD)
- **Multiplayer Issues**: Check your firewall settings
- **Port Issues**: Make sure port 8765 is open for server connections
"""
    
    with open("dist/QUICK_START.md", "w") as f:
        f.write(guide)
    
    print("Quick start guide created")

def create_release_archive():
    """Create a release archive"""
    print("Creating release archive...")
    
    current_platform = platform.system().lower()
    version = "1.0.0"  # You can make this dynamic
    
    if current_platform == "windows":
        archive_name = f"termemoji-v{version}-windows"
        if shutil.which("powershell"):
            run_command(f'powershell -command "Compress-Archive -Path dist/* -DestinationPath {archive_name}.zip"')
        else:
            print("PowerShell not found, skipping archive creation")
    else:
        archive_name = f"termemoji-v{version}-{current_platform}"
        if shutil.which("tar"):
            run_command(f"tar -czf {archive_name}.tar.gz -C dist .")
        else:
            print("tar not found, skipping archive creation")
    
    print(f"Release archive created: {archive_name}")

def main():
    """Main build function"""
    print("=== TermEmoji Release Builder ===")
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    
    # Clean previous builds
    clean_build()
    
    # Build Python package
    if not build_python_package():
        print("Build failed!")
        return 1
    
    # Create standalone scripts
    create_standalone_scripts()
    
    # Create installer scripts
    create_installer_scripts()
    
    # Create quick start guide
    create_quick_start_guide()
    
    # Create release archive
    create_release_archive()
    
    print("\n=== Build Complete ===")
    print("Release files are in the 'dist' directory")
    print("Files created:")
    for root, dirs, files in os.walk("dist"):
        for file in files:
            print(f"  {os.path.join(root, file)}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
