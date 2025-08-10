#!/usr/bin/env python3
"""
Release script for TermEmoji
"""

import os
import sys
import subprocess
import platform
import argparse
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

def build_all_platforms():
    """Build for all platforms"""
    platforms = ['linux', 'windows', 'macos']
    
    for platform_name in platforms:
        print(f"\nBuilding for {platform_name}...")
        
        # Set environment variables for cross-compilation
        env = os.environ.copy()
        if platform_name == 'windows':
            env['PYTHONPATH'] = 'windows'
        elif platform_name == 'macos':
            env['PYTHONPATH'] = 'macos'
        
        # Run build script
        if not run_command([sys.executable, 'build.py'], env=env):
            print(f"Failed to build for {platform_name}")
            return False
    
    return True

def create_github_release(version, description=""):
    """Create a GitHub release"""
    print(f"Creating GitHub release for version {version}...")
    
    # Create git tag
    if not run_command(['git', 'tag', '-a', version, '-m', f'Release {version}']):
        print("Failed to create git tag")
        return False
    
    # Push tag
    if not run_command(['git', 'push', 'origin', version]):
        print("Failed to push git tag")
        return False
    
    print(f"GitHub release {version} created successfully!")
    return True

def main():
    parser = argparse.ArgumentParser(description='Create TermEmoji release')
    parser.add_argument('version', help='Version number (e.g., v1.0.0)')
    parser.add_argument('--description', help='Release description')
    parser.add_argument('--build-only', action='store_true', help='Only build, don\'t create release')
    parser.add_argument('--release-only', action='store_true', help='Only create release, don\'t build')
    
    args = parser.parse_args()
    
    print("TermEmoji Release Script")
    print("=======================")
    
    # Build binaries
    if not args.release_only:
        if not build_all_platforms():
            print("Build failed!")
            return False
    
    # Create GitHub release
    if not args.build_only:
        if not create_github_release(args.version, args.description):
            print("Release creation failed!")
            return False
    
    print("\nRelease process completed successfully!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
