#!/usr/bin/env python3
"""
Setup script for TermEmoji - Terminal-based Emoji Battle Royale Game
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="termemoji",
    version="1.0.0",
    author="TermEmoji Team",
    author_email="",
    description="A terminal-based emoji battle royale game with multiplayer support",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/termemoji",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Games/Entertainment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    python_requires=">=3.8",
    install_requires=[
        "windows-curses; sys_platform == 'win32'",
    ],
    entry_points={
        "console_scripts": [
            "termemoji=main:main",
            "termemoji-server=server:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="game terminal curses multiplayer battle-royale emoji",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/termemoji/issues",
        "Source": "https://github.com/yourusername/termemoji",
        "Documentation": "https://github.com/yourusername/termemoji#readme",
    },
)
