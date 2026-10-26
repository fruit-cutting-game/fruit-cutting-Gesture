[10/26/2026 2:49 PM] CHAN Koemsour WEP A_ 2027: 🍉 Fruit Cutting Gesture Game
A webcam-controlled fruit-cutting game built with Python, OpenCV, MediaPipe, Pygame, and NumPy.
Players use natural hand movements to control a virtual blade and cut fruits on the screen.
📌 Table of Contents
About the Project (https://chatgpt.com/c/6adef4ee-54c8-83ec-b92e-da284e9b3bdb#-about-the-project)
Project Objectives (https://chatgpt.com/c/6adef4ee-54c8-83ec-b92e-da284e9b3bdb#-project-objectives)
Features (https://chatgpt.com/c/6adef4ee-54c8-83ec-b92e-da284e9b3bdb#-features)
Technologies Used (https://chatgpt.com/c/6adef4ee-54c8-83ec-b92e-da284e9b3bdb#-technologies-used)
Project Structure (https://chatgpt.com/c/6adef4ee-54c8-83ec-b92e-da284e9b3bdb#-project-structure)
Installation (https://chatgpt.com/c/6adef4ee-54c8-83ec-b92e-da284e9b3bdb#-installation)
How to Play (https://chatgpt.com/c/6adef4ee-54c8-83ec-b92e-da284e9b3bdb#-how-to-play)
Challenges and Solutions (https://chatgpt.com/c/6adef4ee-54c8-83ec-b92e-da284e9b3bdb#-challenges-and-solutions)
Future Improvements (https://chatgpt.com/c/6adef4ee-54c8-83ec-b92e-da284e9b3bdb#-future-improvements)
🎯 About the Project
Fruit Cutting Gesture Game is an interactive game controlled by hand gestures using a webcam.
Instead of using a mouse or keyboard, players move their hands in front of the camera to control a virtual blade.
The application uses computer vision and hand-tracking technology to detect movements and interact with fruits.
When the virtual blade touches a fruit during a cutting movement, the game checks for a collision and triggers the corresponding action.
🎯 Project Objectives
Develop a game controlled by hand movements.
Detect and track hands using a webcam.
Apply computer vision to interactive gaming.
Create fruit-cutting interactions and visual effects.
Improve Python programming and problem-solving skills.
✨ Features
📷 1. Webcam Control
Captures hand movements through a webcam.
Allows interaction without a traditional controller.
✋ 2. Real-Time Hand Tracking
Uses MediaPipe to track hand landmarks.
Processes hand positions for game control.
🍉 3. Gesture-Based Fruit Cutting
Uses hand movements as a virtual blade.
Detects interactions between the blade and fruits.
💥 4. Collision Detection
Checks whether the blade intersects with fruit objects.
Triggers cutting actions when the conditions are met.
🌟 5. Visual Effects
Displays a blade trail following hand movements.
Supports visual effects for a more engaging experience.
🏆 6. Score System
Tracks the player's score during gameplay.
Displays game information on the screen.
🔊 7. Sound Effects
Uses audio assets to provide feedback during gameplay.
🎮 8. Interactive Game Interface
Renders game objects and interface elements using Pygame.
Combines webcam interaction with real-time gameplay.
🛠 Technologies Used
Technology
Purpose
Python
Main programming language
OpenCV
Camera access and image processing
MediaPipe
Hand tracking
Pygame
Game graphics and audio
NumPy
Numerical calculations
PyInstaller
Creating a Windows executable
📁 Project Structure
Fruit-Cutting-Gesture-Game/
├── main.py
├── src/
│   ├── game.py
│   └── other_modules.py
├── assets/
│   ├── images/
│   ├── fruits/
│   ├── effects/
│   ├── ui/
│   └── sounds/
├── tests/
├── docs/
│   └── project-requirements.docx
├── requirements.txt
└── README.md
This is an example structure. Keep your actual filenames and folders.
🚀 Installation
1. Clone the Repository
git clone YOUR_GITHUB_REPOSITORY_URL
cd YOUR_PROJECT_FOLDER
2. Create a Virtual Environment
python -m venv .venv
3. Activate the Environment
.venv\Scripts\activate
4. Install Dependencies
python -m pip install -r requirements.txt
5. Run the Game
python main.py
[10/26/2026 2:49 PM] CHAN Koemsour WEP A_ 2027: Make sure your webcam is connected and accessible.
🕹 How to Play
Start the application.
Allow access to your webcam if requested.
Position your hand in front of the camera.
Move your hand to control the virtual blade.
Try to cut the fruits on the screen.
Check your score as you play.
Exit the game using its supported exit control.
🧩 Challenges and Solutions
Challenge
Solution
Hand tracking accuracy
Improve lighting and hand positioning
Incorrect cutting detection
Adjust gesture and collision logic
Slow performance
Optimize camera processing and game loops
Missing assets in the EXE
Configure PyInstaller to include required files
🔮 Future Improvements
Add more types of fruits.
Introduce difficulty levels and a timer.
Create a high-score leaderboard.
Add pause and game-over screens.
Improve gesture recognition.
Package the game for Windows.
📚 Learning Outcomes
Through this project, we can learn about:
Python game development.
Computer vision and image processing.
Real-time hand tracking.
Gesture recognition and collision detection.
Game design, testing, and debugging.
Packaging Python applications for Windows.
👨‍💻 Conclusion
Fruit Cutting Gesture Game combines computer vision and game development to create an interactive gaming experience. It demonstrates how webcam-based hand tracking can be used to control game actions and provides opportunities to develop programming and problem-solving skills.
