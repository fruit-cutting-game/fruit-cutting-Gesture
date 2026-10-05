# 🍉 Fruit Cutting Gesture Game (កាត់ផ្លែឈើ)

An interactive, real-time computer vision game developed in Python. Players use hand gestures captured via a webcam to slice virtual fruits floating across the screen.

---

## 📌 Project Overview
This project combines gesture detection with 2D game mechanics to deliver a Fruit Ninja-style experience directly on your computer without additional hardware controllers.

### Key Features
- **Real-Time Hand Tracking**: Uses MediaPipe to detect and track finger and palm gestures via webcam.
- **Gesture Slicing Physics**: Calculates motion velocity and trajectories to register fruit slicing actions accurately.
- **Dynamic Gameplay**: Includes fruit spawning algorithms, collision detection, combo multipliers, score tracking, and lives management.
- **Interactive UI**: Clean heads-up display (HUD) showing scores, remaining lives, and visual feedback for cut effects.

---

## 🛠️ Tech Stack & Tools
- **Language**: Python 3.x
- **Computer Vision**: OpenCV, MediaPipe
- **Game Engine & Rendering**: Pygame
- **Data Processing**: NumPy

---

## 🚀 Getting Started

### Prerequisites
Ensure you have Python 3.8+ installed on your system along with a working webcam.

### Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/fruit-cutting-game/fruit-cutting-Gesture.git](https://github.com/fruit-cutting-game/fruit-cutting-Gesture.git)
   cd fruit-cutting-Gesture
