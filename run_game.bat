
@echo off
cd /d "%~dp0"
".venv312\Scripts\python.exe" main.py
pause


echo ============================================
echo   Fruit Cutting Game - Setup and Run
echo ============================================
echo.

where py >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python Launcher "py" was not found.
    echo Please install Python 3.12 from python.org and enable the Python Launcher.
    pause
    exit /b 1
)

py -3.12 --version >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python 3.12 is not installed.
    echo This game uses MediaPipe's older hand-tracking API.
    echo Install Python 3.12, then double-click this file again.
    echo Download: https://www.python.org/downloads/release/python-31210/
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Creating a dedicated Python 3.12 environment...
    py -3.12 -m venv .venv
    if errorlevel 1 goto failed
)

echo Installing compatible game dependencies...
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto failed
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto failed

echo.
echo Checking MediaPipe hand tracking...
".venv\Scripts\python.exe" -c "import mediapipe as mp; print('MediaPipe', mp.__version__); print('Hands API:', mp.solutions.hands)"
if errorlevel 1 goto failed

echo.
echo Starting Fruit Cutting Game...
".venv\Scripts\python.exe" main.py
if errorlevel 1 goto failed
goto end

:failed
echo.
echo Setup or game launch failed. Please take a screenshot of this window.
pause
exit /b 1

:end
pause
