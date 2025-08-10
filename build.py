#!/usr/bin/env python3
"""
Build script for TermEmoji game and server binaries using PyInstaller
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return the result"""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(f"Success: {result.stdout}")
    return True

def clean_build():
    """Clean previous build artifacts"""
    print("Cleaning previous builds...")
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    
    # Clean .spec files
    for spec_file in Path('.').glob('*.spec'):
        spec_file.unlink()

def build_game():
    """Build the game binary"""
    print("Building game binary...")
    
    # PyInstaller command for the game
    cmd = [
        'pyinstaller',
        '--onefile',
        '--name=termemoji',
        '--add-data=characters.py:.',
        '--add-data=simple_char_select.py:.',
        '--add-data=utils.py:.',
        '--add-data=models.py:.',
        '--add-data=ai.py:.',
        '--add-data=renderer.py:.',
        '--add-data=game_logic.py:.',
        '--add-data=net_client.py:.',
        '--add-data=lobby_screen.py:.',
        '--hidden-import=curses',
        '--hidden-import=queue',
        '--hidden-import=threading',
        '--hidden-import=socket',
        '--hidden-import=json',
        '--hidden-import=time',
        '--hidden-import=random',
        '--hidden-import=math',
        'main.py'
    ]
    
    return run_command(cmd)

def build_server():
    """Build the server binary"""
    print("Building server binary...")
    
    # PyInstaller command for the server
    cmd = [
        'pyinstaller',
        '--onefile',
        '--name=termemoji-server',
        '--hidden-import=socket',
        '--hidden-import=threading',
        '--hidden-import=json',
        '--hidden-import=time',
        '--hidden-import=argparse',
        'server.py'
    ]
    
    return run_command(cmd)

def get_platform_info():
    """Get platform information for naming"""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == 'darwin':
        return 'macos'
    elif system == 'windows':
        return 'windows'
    elif system == 'linux':
        return 'linux'
    else:
        return system

def create_release_package():
    """Create release package with binaries"""
    platform_name = get_platform_info()
    release_dir = f"termemoji-{platform_name}"
    
    # Create release directory
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    os.makedirs(release_dir)
    
    # Copy binaries
    if os.path.exists('dist/termemoji'):
        shutil.copy2('dist/termemoji', f'{release_dir}/termemoji')
    elif os.path.exists('dist/termemoji.exe'):
        shutil.copy2('dist/termemoji.exe', f'{release_dir}/termemoji.exe')
    
    if os.path.exists('dist/termemoji-server'):
        shutil.copy2('dist/termemoji-server', f'{release_dir}/termemoji-server')
    elif os.path.exists('dist/termemoji-server.exe'):
        shutil.copy2('dist/termemoji-server.exe', f'{release_dir}/termemoji-server.exe')
    
    # Copy README and other files
    if os.path.exists('README.md'):
        shutil.copy2('README.md', f'{release_dir}/README.md')
    
    # Create run scripts
    if platform_name == 'windows':
        with open(f'{release_dir}/run-game.bat', 'w') as f:
            f.write('@echo off\n')
            f.write('echo Starting TermEmoji Game...\n')
            f.write('termemoji.exe\n')
            f.write('pause\n')
        
        with open(f'{release_dir}/run-server.bat', 'w') as f:
            f.write('@echo off\n')
            f.write('echo Starting TermEmoji Server...\n')
            f.write('termemoji-server.exe --host 0.0.0.0 --port 8765\n')
            f.write('pause\n')
    else:
        with open(f'{release_dir}/run-game.sh', 'w') as f:
            f.write('#!/bin/bash\n')
            f.write('echo "Starting TermEmoji Game..."\n')
            f.write('./termemoji\n')
        
        with open(f'{release_dir}/run-server.sh', 'w') as f:
            f.write('#!/bin/bash\n')
            f.write('echo "Starting TermEmoji Server..."\n')
            f.write('./termemoji-server --host 0.0.0.0 --port 8765\n')
        
        # Make scripts executable
        os.chmod(f'{release_dir}/run-game.sh', 0o755)
        os.chmod(f'{release_dir}/run-server.sh', 0o755)
    
    # Create archive
    archive_name = f"{release_dir}.zip"
    shutil.make_archive(release_dir, 'zip', release_dir)
    
    print(f"Release package created: {archive_name}")
    return archive_name

def main():
    """Main build function"""
    print("TermEmoji Build Script")
    print("=====================")
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print(f"PyInstaller version: {PyInstaller.__version__}")
    except ImportError:
        print("PyInstaller not found. Installing...")
        if not run_command([sys.executable, '-m', 'pip', 'install', 'pyinstaller']):
            print("Failed to install PyInstaller")
            return False
    
    # Clean previous builds
    clean_build()
    
    # Build game
    if not build_game():
        print("Failed to build game")
        return False
    
    # Build server
    if not build_server():
        print("Failed to build server")
        return False
    
    # Create release package
    archive_name = create_release_package()
    
    print(f"\nBuild completed successfully!")
    print(f"Release package: {archive_name}")
    print(f"Platform: {get_platform_info()}")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
