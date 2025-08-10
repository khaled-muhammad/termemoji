@echo off
echo ========================================
echo TermEmoji - Windows Installation
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo Python found. Installing dependencies...
echo.

echo Installing windows-curses...
python -m pip install --upgrade pip
python -m pip install windows-curses

if errorlevel 1 (
    echo ERROR: Failed to install windows-curses
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo Installing TermEmoji...
python -m pip install -e .

if errorlevel 1 (
    echo ERROR: Failed to install TermEmoji
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo To start the game, run:
echo   python main.py
echo.
echo To start the server, run:
echo   python server.py --host 0.0.0.0 --port 8765
echo.
echo For multiplayer, start the server first, then run the game.
echo.
pause
