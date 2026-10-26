🍉 Fruit Cutting Gesture Game
1. About the Project
Fruit Cutting Gesture Game is an interactive game controlled by hand gestures using a webcam. Instead of using a mouse or keyboard to cut fruits, players can move their hands in front of the camera to control the game.
The system uses computer vision and hand-tracking technology to detect hand movements and recognize gestures. When the player moves their hand across a fruit, the game checks for a collision and cuts the fruit if the movement matches the cutting action.
The game is developed using Python, OpenCV, MediaPipe, Pygame, and NumPy. It combines computer vision, real-time hand tracking, game physics, animations, and sound effects to create an enjoyable gaming experience.
The main goal of this project is to explore how computer vision and gesture recognition can be used to create interactive applications.
2. Project Objectives
Develop a game controlled by natural hand movements.
Use a webcam to capture real-time video.
Track hand landmarks using MediaPipe.
Detect hand movements using OpenCV and Python.
Create fruit-cutting interactions with collision detection.
Add animations, sound effects, and a scoring system.
Improve programming, problem-solving, and computer vision skills.
Explore the integration of AI-related technologies with game development.
3. Main Features
3.1 Webcam-Based Control
Uses a webcam to capture the player's hand movements.
Allows players to interact with the game without a traditional controller.
Processes camera frames in real time.
Provides a more natural and interactive gaming experience.
3.2 Real-Time Hand Tracking
Uses MediaPipe to detect and track hand landmarks.
Tracks hand or finger positions across camera frames.
Converts detected positions into game-control coordinates.
Supports continuous movement while the game is running.
3.3 Gesture-Based Fruit Cutting
Uses hand movement as a virtual blade.
Detects cutting movements across the screen.
Checks whether the virtual blade intersects with fruit objects.
Triggers fruit-cutting effects when a valid collision is detected.
3.4 Fruit Spawning and Movement
Displays fruits that players can cut.
Moves fruit objects across the game screen.
Supports fruit spawning and movement logic.
Provides opportunities to improve reaction speed and accuracy.
3.5 Collision Detection
Checks the interaction between the virtual blade and fruit objects.
Determines when a fruit should be cut.
Helps control fruit-cutting events and scoring.
Connects hand movements with in-game actions.
3.6 Blade Trail Effects
Displays a visual trail following the player's hand movement.
Makes cutting actions easier to see.
Improves the visual feedback of gesture interactions.
Creates a more dynamic gameplay experience.
3.7 Score System
Tracks the player's score during gameplay.
Updates the score when fruit-cutting events are registered.
Displays game information through the user interface.
3.8 Sound Effects
Supports audio assets for game events.
Improves feedback when players interact with fruits.
Makes the gameplay more engaging.
3.9 Game Interface
Uses Pygame to render game graphics and interface elements.
Displays fruits, effects, and game information.
Combines camera-based interaction with traditional game rendering.
3.10 Modular Project Structure
Organizes game logic and helper modules in separate files.
Keeps assets such as images and sounds in dedicated folders.
Makes the code easier to maintain, test, and extend.
Supports future improvements and additional features.
Note: The exact availability of individual features depends on their implementation in the current source code.
4. Technologies Used
Technology
Purpose
Python
Main programming language
OpenCV
Webcam access and image processing
MediaPipe
Real-time hand tracking and landmark detection
Pygame
Game window, graphics, events, and audio
NumPy
Numerical calculations and array operations
PyInstaller
Packaging the Python application into a Windows executable
5. Project Structure
[10/26/2026 2:45 PM] CHAN Koemsour WEP A_ 2027: Fruit-Cutting-Gesture-Game/
│
├── main.py
├── src/
│   ├── game.py
│   ├── camera.py
│   ├── hand_tracking.py
│   ├── gesture_detection.py
│   ├── motion.py
│   ├── blade_trail.py
│   ├── fruit.py
│   ├── collision.py
│   ├── score.py
│   ├── rendering.py
│   ├── audio.py
│   └── config.py
│
├── assets/
│   ├── images/
│   ├── fruits/
│   ├── effects/
│   ├── ui/
│   └── sounds/
│
├── tests/
├── docs/
│   └── project-requirements.docx
│
├── requirements.txt
└── README.md
The module names above illustrate possible responsibilities. Your actual files may have different names inside src/.
6. Installation and Setup (Windows)
Step 1: Install Python
Download and install Python from:
https://www.python.org/downloads/
During installation, enable Add Python to PATH.
Check the installation:
python --version
Step 2: Download the Project
Clone the GitHub repository:
git clone YOUR_GITHUB_REPOSITORY_URL
Alternatively, download the project as a ZIP file and extract it.
Open the project folder:
cd Fruit-Cutting-Gesture-Game
Replace the example folder name with your actual folder name.
Step 3: Create a Virtual Environment
python -m venv .venv
Activate it on Windows:
.venv\Scripts\activate
Step 4: Install Dependencies
If your project includes requirements.txt, run:
python -m pip install -r requirements.txt
If the file is missing, install the packages required by your actual code. For example:
python -m pip install opencv-python mediapipe pygame numpy
Some MediaPipe versions may require a compatible Python version.
Step 5: Run the Game
python main.py
Allow camera access if Windows requests permission.
7. How to Play
Connect a working webcam to your computer.
Start the game using main.py.
Position yourself in front of the webcam.
Place your hand where the camera can clearly see it.
Move your hand across the screen to control the virtual blade.
Try to cut the fruits by moving the blade through them.
Watch the score and visual effects during gameplay.
Close the game using its supported exit control.
The exact controls depend on the gesture and input logic implemented in the project.
8. Creating a Windows EXE File
You can package the game into a Windows executable using PyInstaller.
Step 1: Install PyInstaller
python -m pip install pyinstaller
Step 2: Build the EXE
From the project root folder, run:
python -m PyInstaller --onedir --name FruitCuttingGame --add-data "assets;assets" main.py
This command creates a folder-based application and includes the assets folder.
Step 3: Find the Output
After the build finishes, look inside:
dist/
└── FruitCuttingGame/
    ├── FruitCuttingGame.exe
    └── supporting files
[10/26/2026 2:45 PM] CHAN Koemsour WEP A_ 2027: Run FruitCuttingGame.exe to test it.
Important: Python applications that use OpenCV, MediaPipe, Pygame, and external image or audio files may require additional packaging configuration. The build command may need adjustment based on your installed package versions and how the source code loads its assets.
Test the executable on your computer before sharing it with others. A webcam is also required for gesture control.
9. Challenges and Solutions
Challenge 1: Detecting Hand Movements
Problem: Hand tracking can be affected by lighting, camera quality, and hand position.
Solution: Use adequate lighting, position the hand clearly in the camera view, and tune the tracking settings.
Challenge 2: Accurate Fruit Cutting
Problem: The virtual blade may not register a cutting movement correctly.
Solution: Improve gesture detection, motion tracking, and collision-detection logic.
Challenge 3: Game Performance
Problem: Processing webcam frames while rendering the game can affect performance.
Solution: Optimize image processing, avoid unnecessary calculations, and keep the game loop efficient.
Challenge 4: Organizing Project Files
Problem: Managing Python modules, images, and sound files can become difficult as the project grows.
Solution: Separate the code into modules and organize assets into dedicated folders.
Challenge 5: Creating an EXE File
Problem: The executable may fail to find assets or load dependencies after packaging.
Solution: Configure PyInstaller to include the necessary assets and dependencies, and test the packaged application.
10. Future Improvements
Add different difficulty levels.
Introduce more fruit types and cutting effects.
Add a timer and countdown system.
Create a high-score leaderboard.
Add a start menu, pause menu, and game-over screen.
Improve hand-tracking accuracy.
Add background music and more sound effects.
Add a settings menu for camera and audio options.
Improve performance on lower-end computers.
Package the game into an easy-to-install Windows application.
These are potential improvements and should not be considered existing features unless they have been implemented.
11. Learning Outcomes
Through this project, we can learn how to:
Use Python to develop an interactive game.
Access a webcam using OpenCV.
Track hand landmarks using MediaPipe.
Process movement and recognize gestures.
Implement collision detection and scoring logic.
Work with images, audio, and animations in Pygame.
Organize code into reusable modules.
Debug software problems and test game behavior.
Package a Python project for Windows using PyInstaller.
12. Conclusion
The Fruit Cutting Gesture Game demonstrates how computer vision and game development can work together to create an interactive experience. By using webcam input, hand tracking, and gesture-based controls, the project allows players to interact with a game through natural hand movements.
This project also provides practical experience with Python, OpenCV, MediaPipe, Pygame, and NumPy. In the future, it can be improved with more gameplay features, better performance, and easier installation.
13. License
Choose an appropriate open-source license before publishing the project. Make sure that any third-party images, sounds, and other assets are permitted for your intended use.
