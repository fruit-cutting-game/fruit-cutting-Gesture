# Fruit Cutting Gesture Game

A webcam-controlled fruit-cutting game using Python, OpenCV, MediaPipe, Pygame and NumPy.

## Project structure

- `main.py` — application entry point
- `src/game.py` — existing complete game implementation (kept together to preserve current behavior)
- `src/` — modular helpers for camera, hand tracking, motion, gesture detection, blade trail, fruit, collision, score, state, rendering, audio and configuration
- `assets/images/` — compatibility asset directory used by the current game
- `assets/fruits/`, `assets/effects/`, `assets/ui/` — categorized copies for future modular development
- `assets/sounds/` — sound files
- `tests/` — automated tests
- `docs/project-requirements.docx` — project requirements

## Setup (Windows)

**Recommended: use the included `run_game.bat`.** Double-click it to create a separate Python 3.12 environment, install compatible dependencies, test MediaPipe, and start the game. This avoids using the incompatible MediaPipe package installed for Python 3.13.

Python 3.12 must be installed with the Python Launcher (`py`). If it is not installed, install Python 3.12 first, then double-click `run_game.bat` again.

Manual setup in PowerShell:

```powershell
py -3.12 -m venv .venv
.\\.venv\\Scripts\\python.exe -m pip install --upgrade pip
.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt
.\\.venv\\Scripts\\python.exe main.py
```

Make sure your webcam is connected and allowed by Windows privacy settings.

## Note

The original game loop and its existing classes are kept in `src/game.py` to avoid accidentally breaking the game during the first structural refactor. The helper modules are separated and ready for incremental integration; the entire game logic has not yet been fully redistributed across every module.
