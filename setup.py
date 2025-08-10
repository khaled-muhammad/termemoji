#!/usr/bin/env python3
"""
Setup script for TermEmoji
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    if os.path.exists('README.md'):
        with open('README.md', 'r', encoding='utf-8') as f:
            return f.read()
    return "TermEmoji - Terminal-based emoji battle royale game"

setup(
    name="termemoji",
    version="1.0.0",
    author="TermEmoji Team",
    description="A terminal-based emoji battle royale game with multiplayer support",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/termemoji",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Games/Entertainment",
        "Topic :: Terminals",
    ],
    python_requires=">=3.9",
    install_requires=[],
    entry_points={
        'console_scripts': [
            'termemoji=main:main',
            'termemoji-server=server:main',
        ],
    },
    include_package_data=True,
    package_data={
        '': ['*.py'],
    },
)
