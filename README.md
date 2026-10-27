# 🍉 Fruit Cutting Gesture Game

A webcam-controlled fruit-cutting game built with **Python, OpenCV, MediaPipe, Pygame, and NumPy**. Players use hand gestures in front of a webcam to cut fruits, avoid bombs, and earn points.

## 🎮 Game Features

- **Hand Gesture Control:** Use your hand in front of the webcam to control the blade.
- **Fruit Cutting:** Cut different types of fruits to earn points.
- **Bomb System:** Avoid bombs to protect your lives.
- **Special Items:** Collect special items such as hearts and boxes.
- **Difficulty Levels:** Choose Easy, Medium, or Hard.
- **Scoring System:** Earn points by cutting fruits.
- **Lives System:** Keep playing while you have lives remaining.
- **Sound Effects:** Enjoy background music and game sound effects.
- **Interactive Menu:** Navigate the Home, Settings, How to Play, and game screens.
- **Game Controls:** Start, pause or exit the game using the available interface controls.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| OpenCV | Webcam and camera image processing |
| MediaPipe | Hand tracking and gesture detection |
| Pygame | Game window, graphics, events, and audio |
| NumPy | Numerical operations and image processing |
| Git and GitHub | Version control and teamwork |

## 📁 Project Structure

```text
fruit-cutting-Gesture/
│
├── main.py
├── src/
│   ├── game.py
│   └── camera, gesture, motion, collision,
│       rendering, audio, and configuration modules
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
├── requirements.txt
├── run_game.bat
└── README.md
```

*Note: Adjust the structure above to match the actual files and folders in your repository.*

## 💻 Requirements

- Windows 10 or Windows 11
- Python 3.12 (recommended for your current project environment)
- A webcam
- Git (optional, for cloning the project)

## ⚙️ Installation and Setup (Windows)

### 1. Clone the repository

Open Git Bash or a terminal and run:

```bash
git clone YOUR_REPOSITORY_URL
cd fruit-cutting-Gesture
```

Replace `YOUR_REPOSITORY_URL` with your actual GitHub repository URL.

### 2. Create a virtual environment

```bash
py -3.12 -m venv .venv
```

### 3. Activate the virtual environment

For Command Prompt:

```bat
.venv\Scripts\activate
```

For Git Bash:

```bash
source .venv/Scripts/activate
```

### 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Make sure `requirements.txt` contains the compatible versions of the libraries used by the project.

### 5. Run the game

```bash
python main.py
```

You can also run the game using `run_game.bat` if the batch file is configured correctly.

## 🕹️ How to Play

1. Connect your webcam.
2. Start the game and allow camera access.
3. Choose a difficulty level.
4. Place your hand in front of the webcam.
5. Move your hand to control the blade and cut the fruits.
6. Avoid bombs to protect your lives.
7. Collect special items when they appear.
8. Try to achieve the highest score!

## 📊 Game Rules

- Cut fruits to earn points.
- Avoid bombs to prevent losing lives or triggering bomb effects.
- Collect special items when available.
- Try to keep your lives and achieve a high score.
- The game ends when the game-over condition is reached.

*The exact scoring and bomb penalties depend on the current game implementation.*

## 👨‍💻 Teamwork and Development

This project is developed as part of an algorithm and programming learning project.

Git and GitHub help team members collaborate through branches, commits, and merges. New features can be developed on separate branches and merged into the `main` branch after testing.

## 🚀 Future Improvements

- Improve hand-tracking accuracy.
- Add more fruits and special effects.
- Improve game performance.
- Add a high-score leaderboard.
- Add more game modes.
- Improve the user interface and user experience.
- Expand automated test coverage.

## 📄 Project Documentation

Project requirements and related documentation are available in the `docs/` directory.

## 🙌 Acknowledgments

Thanks to our teachers and teammates for their guidance, feedback, and collaboration during development.

---

**Enjoy playing Fruit Cutting Gesture Game! 🍎🍌🍉**

