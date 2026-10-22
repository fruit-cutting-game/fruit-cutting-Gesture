
@echo off
cd /d "%~dp0"
title Fruit Cutting Gesture Game

echo ========================================
echo     FRUIT CUTTING GESTURE GAME
echo ========================================
echo.

if not exist "main.py" (
    echo ERROR: main.py not found in this folder!
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Creating Python environment...
    py -3.12 -m venv .venv

    if errorlevel 1 (
        echo ERROR: Python 3.12 is not installed.
        echo Please install Python 3.12 and try again.
        pause
        exit /b 1
    )
)

echo Installing required libraries...
".venv\Scripts\python.exe" -m pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Could not install required libraries.
    pause
    exit /b 1
)

echo.
echo Starting Fruit Cutting Game...
".venv\Scripts\python.exe" main.py

echo.
echo Game closed.
pause
