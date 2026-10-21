
@echo off
cd /d "%~dp0"

echo Starting Fruit Cutting Game...
echo.

if not exist "main.py" (
    echo ERROR: main.py was not found!
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo ERROR: Python environment not found!
    echo Please set up Python and install the required libraries.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" main.py

pause
