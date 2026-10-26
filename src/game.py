import cv2

import mediapipe as mp

import random

import math

import os

import collections

import time

import pygame

import numpy as np
import json
from datetime import datetime


# 0. Initialize Pygame Mixer for Audio

pygame.mixer.init()



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ASSET_FOLDER = os.path.join(BASE_DIR, "assets")

SOUND_FOLDER = os.path.join(ASSET_FOLDER, "sounds")


# ================= SCORE HISTORY =================
HISTORY_FILE = os.path.join(BASE_DIR, "score_history.json")
MAX_HISTORY_RECORDS = 10


def load_score_history():
    """Load the saved game records from the JSON file."""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            if isinstance(data, list):
                return data[:MAX_HISTORY_RECORDS]

    except (json.JSONDecodeError, OSError):
        print("Warning: Could not read score history.")

    return []


def save_score_history(records):
    """Save only the latest 10 game records."""
    records = records[:MAX_HISTORY_RECORDS]

    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            json.dump(records, file, indent=4)
    except OSError as error:
        print(f"Could not save score history: {error}")


def record_completed_game(final_score, difficulty, elapsed_seconds):
    """Save one completed game without deleting older records."""
    records = load_score_history()

    record = {
        "score": int(final_score),
        "difficulty": str(difficulty),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "time_survived": int(max(0, elapsed_seconds))
    }

    records.insert(0, record)
    save_score_history(records)
# Load Sound Effects

slice_sound = None

boom_sound = None

bigboom_sound = None

surprise_sound = None



slice_path = os.path.join(SOUND_FOLDER, "cutting fruit.mp3")

boom_path = os.path.join(SOUND_FOLDER, "boom.mp3")

bigboom_path = os.path.join(SOUND_FOLDER, "bigboom.mp3")

surprise_path = os.path.join(SOUND_FOLDER, "Surprise.mp3")

bg_music_path = os.path.join(SOUND_FOLDER, "sounds game.mp3")



if os.path.exists(slice_path):

    slice_sound = pygame.mixer.Sound(slice_path)

    slice_sound.set_volume(0.6)



if os.path.exists(boom_path):

    boom_sound = pygame.mixer.Sound(boom_path)

    boom_sound.set_volume(0.3)



if os.path.exists(bigboom_path):

    bigboom_sound = pygame.mixer.Sound(bigboom_path)

    bigboom_sound.set_volume(1.0)



if os.path.exists(surprise_path):

    surprise_sound = pygame.mixer.Sound(surprise_path)

    surprise_sound.set_volume(0.3)



# Play Background Music

if os.path.exists(bg_music_path):

    pygame.mixer.music.load(bg_music_path)

    pygame.mixer.music.set_volume(0.4)

    pygame.mixer.music.play(-1)



# 1. Initialize MediaPipe Hand Tracking

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(

    static_image_mode=False,

    max_num_hands=1,

    min_detection_confidence=0.5,

    min_tracking_confidence=0.5

)



# 2. Load Images from "images" folder

IMAGE_FOLDER = os.path.join(ASSET_FOLDER, "images")


fruit_files = {
    "apple": "apple.png",
    "banana": "banana.png",
    "grape": "grape.png",
    "orange": "orange.png",
    "pineapple": "pineapple.png",
    "watermelon": "watermelon.png",
    "peach": "peach.png",
    "mango": "mango.png"
}

fruit_images = {}

for name, filename in fruit_files.items():
    path = os.path.join(IMAGE_FOLDER, filename)
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)

    if img is not None:
        fruit_images[name] = img
    else:
        print(f"Warning: Could not load fruit image: {path}")

splash_images = {
    "yellow": cv2.imread(
        os.path.join(IMAGE_FOLDER, "yellow.png"),
        cv2.IMREAD_UNCHANGED
    ),
    "red": cv2.imread(
        os.path.join(IMAGE_FOLDER, "red.png"),
        cv2.IMREAD_UNCHANGED
    ),
    "blue": cv2.imread(
        os.path.join(IMAGE_FOLDER, "blue.png"),
        cv2.IMREAD_UNCHANGED
    )
}

fruit_splash_map = {
    "orange": "yellow",
    "pineapple": "yellow",
    "banana": "yellow",
    "mango": "yellow",
    "apple": "red",
    "watermelon": "red",
    "peach": "red",
    "grape": "blue"
}




# Load Boom Images

boom1_img = cv2.imread(os.path.join(IMAGE_FOLDER, "boom1.png"), cv2.IMREAD_UNCHANGED)

boom2_img = cv2.imread(os.path.join(IMAGE_FOLDER, "boom2.png"), cv2.IMREAD_UNCHANGED)

boom3_img = cv2.imread(os.path.join(IMAGE_FOLDER, "boom3.png"), cv2.IMREAD_UNCHANGED)

boom4_img = cv2.imread(os.path.join(IMAGE_FOLDER, "boom4.png"), cv2.IMREAD_UNCHANGED)



# Load Treasure Box Images

box1_img = cv2.imread(os.path.join(IMAGE_FOLDER, "box1.png"), cv2.IMREAD_UNCHANGED)

box2_img = cv2.imread(os.path.join(IMAGE_FOLDER, "box2.png"), cv2.IMREAD_UNCHANGED)



# Load Heart Images

heart1_img = cv2.imread(os.path.join(IMAGE_FOLDER, "heart1.png"), cv2.IMREAD_UNCHANGED)

heart2_img = cv2.imread(os.path.join(IMAGE_FOLDER, "heart2.png"), cv2.IMREAD_UNCHANGED)



# Load Control Buttons Images (ប្រើ startgame.png និង stop.png)

home_btn_img = cv2.imread(os.path.join(IMAGE_FOLDER, "home.png"), cv2.IMREAD_UNCHANGED)

startgame_btn_img = cv2.imread(os.path.join(IMAGE_FOLDER, "startgame.png"), cv2.IMREAD_UNCHANGED)

stop_btn_img = cv2.imread(os.path.join(IMAGE_FOLDER, "stop.png"), cv2.IMREAD_UNCHANGED)

restart_btn_img = cv2.imread(os.path.join(IMAGE_FOLDER, "restart.png"), cv2.IMREAD_UNCHANGED)



sword_img = cv2.imread(os.path.join(IMAGE_FOLDER, "sword.png"), cv2.IMREAD_UNCHANGED)

point_img = cv2.imread(os.path.join(IMAGE_FOLDER, "point.png"), cv2.IMREAD_UNCHANGED)



life_image_files = [

    "dog1.png",

    "dog2.png",

    "tiger.png",

    "monkey1.png",

    "monkey2.png"

]



life_images = []

for file_name in life_image_files:

    path = os.path.join(IMAGE_FOLDER, file_name)

    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)

    life_images.append(img)



bg_img_path = os.path.join(IMAGE_FOLDER, "Attack on Titan.png")

bg_img_raw = cv2.imread(bg_img_path)



last_big_bomb_time = time.time()

last_box_time = time.time()

last_heart_time = time.time()

game_start_time = 0

paused_duration = 0

pause_start_time = 0

is_paused = False



# Overlay PNG Function

def overlay_png(background, overlay, x, y, size=90, crop_side=None, alpha_factor=1.0, angle=0):

    if overlay is None:

        return



    if crop_side == "left":

        overlay_cut = overlay[:, :overlay.shape[1]//2]

    elif crop_side == "right":

        overlay_cut = overlay[:, overlay.shape[1]//2:]

    else:

        overlay_cut = overlay



    h_orig, w_orig = overlay_cut.shape[:2]

    aspect = w_orig / h_orig

    target_w = int(size * aspect)

    target_h = size



    if target_w <= 0 or target_h <= 0:

        return



    overlay_resized = cv2.resize(overlay_cut, (target_w, target_h))



    if angle != 0:

        center = (target_w // 2, target_h // 2)

        M = cv2.getRotationMatrix2D(center, angle, 1.0)

        overlay_resized = cv2.warpAffine(

            overlay_resized, M, (target_w, target_h),

            flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0,0)

        )



    h, w, c = overlay_resized.shape



    top_x = int(x - w / 2)

    top_y = int(y - h / 2)



    bg_h, bg_w, _ = background.shape



    x1, x2 = max(0, top_x), min(bg_w, top_x + w)

    y1, y2 = max(0, top_y), min(bg_h, top_y + h)



    overlay_x1, overlay_x2 = max(0, -top_x), w - max(0, (top_x + w) - bg_w)

    overlay_y1, overlay_y2 = max(0, -top_y), h - max(0, (top_y + h) - bg_h)



    if x1 >= x2 or y1 >= y2:

        return



    crop_overlay = overlay_resized[overlay_y1:overlay_y2, overlay_x1:overlay_x2]



    if c == 4:

        alpha = (crop_overlay[:, :, 3] / 255.0) * alpha_factor

        for i in range(3):

            background[y1:y2, x1:x2, i] = (

                alpha * crop_overlay[:, :, i] + (1 - alpha) * background[y1:y2, x1:x2, i]

            )

    else:

        background[y1:y2, x1:x2] = crop_overlay[:, :, :3]



class JuiceSplash:

    def __init__(self, x, y, color_name):

        self.x = x

        self.y = y

        self.img = splash_images.get(color_name, None)

        self.life = 25

        self.size = 180



    def update_and_draw(self, frame):

        if self.life > 0 and self.img is not None:

            overlay_png(frame, self.img, self.x, self.y, size=self.size, alpha_factor=1.0)

            self.life -= 1



class OpenedBoxEffect:

    def __init__(self, x, y):

        self.x = int(x)

        self.y = int(y)

        self.img = box2_img

        self.life = 30

        self.size = 130



    def update_and_draw(self, frame):

        if self.life > 0:

            self.life -= 1

            self.y -= 1

            if self.img is not None:

                overlay_png(frame, self.img, self.x, self.y, self.size, alpha_factor=max(0.2, self.life / 30.0))



            cv2.putText(frame, "+200", (self.x - 40, self.y - 50), 

                        cv2.FONT_HERSHEY_DUPLEX, 1.2, (0, 255, 255), 3)



class HeartCollectedEffect:

    def __init__(self, x, y):

        self.x = int(x)

        self.y = int(y)

        self.img = heart2_img

        self.life = 30

        self.size = 110



    def update_and_draw(self, frame):

        if self.life > 0:

            self.life -= 1

            self.y -= 1

            if self.img is not None:

                overlay_png(frame, self.img, self.x, self.y, self.size, alpha_factor=max(0.2, self.life / 30.0))



            cv2.putText(frame, "+1 LIFE", (self.x - 50, self.y - 50), 

                        cv2.FONT_HERSHEY_DUPLEX, 1.1, (0, 255, 0), 3)



class Fruit:

    def __init__(self, screen_width, screen_height, speed_mult=1.0, allow_special=True):

        self.w = screen_width

        self.h = screen_height

        self.speed_mult = speed_mult

        self.allow_special = allow_special

        self.fruit_names = list(fruit_images.keys()) if fruit_images else []

        self.is_bomb = False

        self.is_big_bomb = False

        self.is_box = False

        self.is_heart = False

        self.name = "apple"

        self.reset()



    def reset(self):

        global last_big_bomb_time, last_box_time, last_heart_time

        current_time = time.time()



        can_spawn_heart = (current_time - last_heart_time) >= 20.0

        can_spawn_big_bomb = (current_time - last_big_bomb_time) >= 15.0

        can_spawn_box = (current_time - last_box_time) >= 10.0



        if self.allow_special and can_spawn_heart:

            self.is_bomb = False

            self.is_big_bomb = False

            self.is_box = False

            self.is_heart = True

            self.img = heart1_img

            self.size = 100

            last_heart_time = current_time

        elif self.allow_special and can_spawn_box:

            self.is_bomb = False

            self.is_big_bomb = False

            self.is_box = True

            self.is_heart = False

            self.img = box1_img

            self.size = 110

            last_box_time = current_time

        elif self.allow_special and can_spawn_big_bomb:

            self.is_bomb = True

            self.is_big_bomb = True

            self.is_box = False

            self.is_heart = False

            self.img = boom3_img

            self.size = 180

            last_big_bomb_time = current_time

        else:

            rand_val = random.random()

            if rand_val < 0.25:

                self.is_bomb = True

                self.is_big_bomb = False

                self.is_box = False

                self.is_heart = False

                self.img = boom1_img

                self.size = 95

            else:

                self.is_bomb = False

                self.is_big_bomb = False

                self.is_box = False

                self.is_heart = False

                if self.fruit_names:

                    self.name = random.choice(self.fruit_names)

                    self.img = fruit_images.get(self.name, None)

                self.size = random.randint(85, 110)



        self.radius = self.size // 2

        self.x = random.randint(120, self.w - 120)

        self.y = self.h + 50



        base_speed = random.randint(16, 22)

        self.speed_y = base_speed * self.speed_mult

        self.speed_x = random.randint(-4, 4)

        self.gravity = 0.55



    def update(self):

        self.x += self.speed_x

        self.y -= self.speed_y

        self.speed_y -= self.gravity

        self.was_reset = False



        if self.y > self.h + 80:

            self.reset()

            self.was_reset = True



    def draw(self, frame):

        ix, iy = int(self.x), int(self.y)

        if self.img is not None:

            overlay_png(frame, self.img, ix, iy, self.size)

        else:

            cv2.circle(frame, (ix, iy), self.radius, (0, 255, 255), -1)



class SplitHalf:

    def __init__(self, x, y, img, size):

        self.x = x

        self.y = y

        self.img = img

        self.size = size

        self.vy = -3

        self.left_vx = -7

        self.right_vx = 7

        self.life = 18

        self.gravity = 0.7



    def update_and_draw(self, frame):

        if self.life > 0:

            self.vy += self.gravity

            self.y += self.vy

            self.life -= 1



            lx = int(self.x + self.left_vx * (19 - self.life))

            rx = int(self.x + self.right_vx * (19 - self.life))

            cy = int(self.y)



            if self.img is not None:

                overlay_png(frame, self.img, lx, cy, self.size, crop_side="left")

                overlay_png(frame, self.img, rx, cy, self.size, crop_side="right")



class BoomExplosion:

    def __init__(self, x, y, is_big=False):

        self.x = int(x)

        self.y = int(y)

        self.life = 25

        self.is_big = is_big



        if is_big:

            self.img = boom4_img

            self.size = 320

        else:

            self.img = boom2_img

            self.size = 140



    def update_and_draw(self, frame):

        if self.life > 0:

            self.life -= 1

            if self.img is not None:

                overlay_png(frame, self.img, self.x, self.y, self.size)

            else:

                cv2.circle(frame, (self.x, self.y), 60, (0, 0, 255), -1)



cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)



ret, webcam_frame = cap.read()

h, w, c = webcam_frame.shape



def maybe_spawn_extra_fruit(primary):

    # ផ្លែទី 2 អាចជាផ្លែឈើ ឬគ្រាប់បែកតូច boom1.png

    # ហើយចេញជិតៗគ្នា និងមិនយឺតជាងផ្លែទី 1

    if primary.is_bomb or primary.is_box or primary.is_heart:

        return None

    if random.random() >= 0.90:

        return None



    extra = Fruit(primary.w, primary.h, primary.speed_mult, allow_special=False)



    # 25% អាចចេញជា boom1.png, មិនប្រើ boom3.png

    if random.random() < 0.25:

        extra.is_bomb = True

        extra.is_big_bomb = False

        extra.is_box = False

        extra.is_heart = False

        extra.img = boom1_img

        extra.size = 95

    else:

        extra.is_bomb = False

        extra.is_big_bomb = False

        extra.is_box = False

        extra.is_heart = False

        if extra.fruit_names:

            extra.name = random.choice(extra.fruit_names)

            extra.img = fruit_images.get(extra.name, None)

        extra.size = random.randint(85, 110)



    extra.radius = extra.size // 2



    # ចេញជិតគ្នា និងល្បឿនស្មើ ឬលឿនជាងផ្លែទី 1 បន្តិច

    extra.x = max(120, min(primary.w - 120, primary.x + random.randint(-65, 65)))

    extra.y = primary.y + random.randint(-12, 12)

    extra.speed_y = max(10, primary.speed_y * random.uniform(1.00, 1.06))

    extra.speed_x = primary.speed_x + random.randint(-2, 2)

    return extra



window_name = "Fruit Ninja - Hand Tracking"

cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)



def draw_rounded_rect(
    frame,
    rect,
    fill_color,
    border_color=(0, 0, 255),
    thickness=2,
    radius=15
):
    x1, y1, x2, y2 = map(int, rect)
    height, width = frame.shape[:2]

    x1 = max(0, min(x1, width - 1))
    x2 = max(0, min(x2, width - 1))
    y1 = max(0, min(y1, height - 1))
    y2 = max(0, min(y2, height - 1))

    if x2 <= x1 or y2 <= y1:
        return

    radius = max(1, min(radius, (x2 - x1) // 2, (y2 - y1) // 2))

    # Fill the rounded rectangle
    cv2.rectangle(
        frame, (x1 + radius, y1), (x2 - radius, y2),
        fill_color, -1, cv2.LINE_AA
    )
    cv2.rectangle(
        frame, (x1, y1 + radius), (x2, y2 - radius),
        fill_color, -1, cv2.LINE_AA
    )

    for px, py in [
        (x1 + radius, y1 + radius),
        (x2 - radius, y1 + radius),
        (x1 + radius, y2 - radius),
        (x2 - radius, y2 - radius)
    ]:
        cv2.circle(frame, (px, py), radius, fill_color, -1, cv2.LINE_AA)

    # Rounded red outline
    cv2.line(frame, (x1 + radius, y1), (x2 - radius, y1),
             border_color, thickness, cv2.LINE_AA)
    cv2.line(frame, (x1 + radius, y2), (x2 - radius, y2),
             border_color, thickness, cv2.LINE_AA)
    cv2.line(frame, (x1, y1 + radius), (x1, y2 - radius),
             border_color, thickness, cv2.LINE_AA)
    cv2.line(frame, (x2, y1 + radius), (x2, y2 - radius),
             border_color, thickness, cv2.LINE_AA)

    cv2.ellipse(frame, (x1 + radius, y1 + radius),
                (radius, radius), 0, 180, 270,
                border_color, thickness, cv2.LINE_AA)
    cv2.ellipse(frame, (x2 - radius, y1 + radius),
                (radius, radius), 0, 270, 360,
                border_color, thickness, cv2.LINE_AA)
    cv2.ellipse(frame, (x2 - radius, y2 - radius),
                (radius, radius), 0, 0, 90,
                border_color, thickness, cv2.LINE_AA)
    cv2.ellipse(frame, (x1 + radius, y2 - radius),
                (radius, radius), 0, 90, 180,
                border_color, thickness, cv2.LINE_AA)


def draw_styled_button(frame, rect, text, base_color, is_hover=False):
    x1, y1, x2, y2 = rect

    if is_hover:
        x1 -= 4
        y1 -= 3
        x2 += 4
        y2 += 3
        fill_color = tuple(min(255, int(c) + 35) for c in base_color)
        text_color = (0, 255, 255)
    else:
        fill_color = base_color
        text_color = (255, 255, 255)

    draw_rounded_rect(
        frame,
        (x1, y1, x2, y2),
        fill_color,
        border_color=(0, 0, 255),
        thickness=2 if not is_hover else 3,
        radius=15
    )

    font = cv2.FONT_HERSHEY_DUPLEX
    scale = 0.75 if is_hover else 0.68
    thickness = 2

    (text_w, text_h), _ = cv2.getTextSize(
        text, font, scale, thickness
    )

    text_x = x1 + (x2 - x1 - text_w) // 2
    text_y = y1 + (y2 - y1 + text_h) // 2

    cv2.putText(
        frame, text, (text_x + 2, text_y + 2),
        font, scale, (0, 0, 0), thickness + 1, cv2.LINE_AA
    )
    cv2.putText(
        frame, text, (text_x, text_y),
        font, scale, text_color, thickness, cv2.LINE_AA
    )



def draw_jet_trail(frame, jet_x, jet_y, angle):

    tail_distance = 55

    rad = math.radians(angle)



    tail_x = int(jet_x - tail_distance * math.cos(rad))

    tail_y = int(jet_y - tail_distance * math.sin(rad))



    flame_flicker = random.randint(-15, 25)

    flame_length = 170 + flame_flicker



    end_x = int(tail_x - flame_length * math.cos(rad))

    end_y = int(tail_y - flame_length * math.sin(rad))



    cv2.line(frame, (tail_x, tail_y), (end_x, end_y), (0, 30, 255), 12)

    cv2.line(frame, (tail_x, tail_y), (end_x, end_y), (0, 140, 255), 8)

    cv2.line(frame, (tail_x, tail_y), (end_x, end_y), (0, 235, 255), 4)

    cv2.line(frame, (tail_x, tail_y), (end_x, end_y), (255, 255, 255), 2)



    for _ in range(3):

        p_dist = random.randint(10, flame_length + 20)

        p_x = int(tail_x - p_dist * math.cos(rad) + random.randint(-3, 3))

        p_y = int(tail_y - p_dist * math.sin(rad) + random.randint(-3, 3))

        p_size = random.randint(1, 3)

        cv2.circle(frame, (p_x, p_y), p_size, (0, random.randint(180, 255), 255), -1)



def draw_point_cursor(frame, x, y):

    if point_img is not None:

        overlay_png(frame, point_img, x, y, size=110)

    else:

        cv2.circle(frame, (x, y), 12, (0, 255, 255), -1)



def show_auto_stretched(win_name, img_frame):

    try:

        rect = cv2.getWindowImageRect(win_name)

        win_w, win_h = rect[2], rect[3]

        if win_w > 0 and win_h > 0:

            resized_frame = cv2.resize(img_frame, (win_w, win_h))

            cv2.imshow(win_name, resized_frame)

            return

    except:

        pass

    cv2.imshow(win_name, img_frame)



last_click_target = None

last_click_time = 0



def check_double_click(target_name):

    global last_click_target, last_click_time

    current_time = time.time()



    if last_click_target == target_name and (0.12 < current_time - last_click_time < 0.85):

        last_click_target = None

        last_click_time = 0

        return True

    else:

        last_click_target = target_name

        last_click_time = current_time

        return False



menu_page = "HOME"
game_state = "MENU"

speed_multiplier = 1.0



score = 0

lives = 5

# Multiple fruits can appear at the same time
fruit = Fruit(w, h, speed_multiplier)
extra_fruit = None
fruits = [fruit]

# Game effects
splits = []
boom_effects = []
box_effects = []
heart_effects = []
splashes = []

# Hand tracking trail
finger_trail = collections.deque(maxlen=12)

# Fruit spawning settings
MAX_FRUITS = 8
FRUIT_SPAWN_INTERVAL = 0.45
last_fruit_spawn_time = time.time()
jet_angle = -90

shuriken_spin_angle = 0  # Extra rotation for the shuriken



# Responsive horizontal menu layout
btn_easy = (w//2 - 330, 315, w//2 - 115, 390)
btn_med  = (w//2 - 107, 315, w//2 + 108, 390)
btn_hard = (w//2 + 116, 315, w//2 + 331, 390)

btn_howto = (w // 2 - 310, 435, w // 2 - 105, 495)
btn_settings = (w // 2 - 100, 435, w // 2 + 100, 495)
btn_quit = (w // 2 + 105, 435, w // 2 + 310, 495)
btn_back = (w // 2 - 120, 550, w // 2 + 120, 605)
btn_history = (w // 2 - 120, 510, w // 2 + 120, 565)
music_enabled = True
sound_effects_enabled = True
vibration_enabled = True
selected_difficulty = "EASY"



ctrl_box_x1, ctrl_box_y1 = 20, h - 90

ctrl_box_x2, ctrl_box_y2 = 230, h - 20



btn_home_rect = (30, h - 80, 85, h - 30)

btn_toggle_rect = (97, h - 80, 152, h - 30)  # ប្រអប់ប៊ូតុងកណ្តាល (សម្រាប់ startgame.png / stop.png)

btn_restart_rect = (165, h - 80, 220, h - 30)



while True:

    # Rotate the shuriken continuously (degrees per frame).

    shuriken_spin_angle = (shuriken_spin_angle + 35) % 360



    ret, webcam_frame = cap.read()

    if not ret:

        break



    webcam_frame = cv2.flip(webcam_frame, 1)



    if bg_img_raw is not None:

        frame = cv2.resize(bg_img_raw, (w, h))

    else:

        frame = webcam_frame.copy()



    rgb_frame = cv2.cvtColor(webcam_frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)

    cx, cy = -1, -1



    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            cx, cy = int(index_tip.x * w), int(index_tip.y * h)

            finger_trail.appendleft((cx, cy))

    else:

        finger_trail.clear()



    if len(finger_trail) >= 3:

        dx = finger_trail[0][0] - finger_trail[2][0]

        dy = finger_trail[0][1] - finger_trail[2][1]



        if math.hypot(dx, dy) > 15:

            target_angle = math.degrees(math.atan2(dy, dx))

            jet_angle = target_angle



    if game_state == "QUIT":
        break
    if game_state == "MENU":
        panel_left, panel_top = 120, 35
        panel_right, panel_bottom = w - 120, h - 30

        # Premium dark menu panel
        for gy in range(panel_top, panel_bottom, 4):
            t = (gy - panel_top) / max(1, panel_bottom - panel_top)
            shade = int(18 + 10 * t)
            cv2.line(
                frame, (panel_left, gy), (panel_right, gy),
                (shade, shade // 2, shade + 13), 4
            )

        cv2.rectangle(
            frame, (panel_left, panel_top),
            (panel_right, panel_bottom), (75, 58, 115), 2
        )
        cv2.line(
            frame, (panel_left + 35, panel_top + 8),
            (panel_right - 35, panel_top + 8), (0, 210, 255), 2
        )

        # ================= HOME PAGE =================
        if menu_page == "HOME":
            title = "FRUIT SLASH"
            font = cv2.FONT_HERSHEY_DUPLEX
            title_size = 1.75
            title_thickness = 4

            (title_w, _), _ = cv2.getTextSize(
                title, font, title_size, title_thickness
            )
            title_x = (w - title_w) // 2

            cv2.putText(
                frame, title, (title_x, 135), font,
                title_size, (0, 120, 180), 10, cv2.LINE_AA
            )
            cv2.putText(
                frame, title, (title_x, 135), font,
                title_size, (0, 235, 255), title_thickness,
                cv2.LINE_AA
            )

            subtitle = "HAND GESTURE EDITION"
            (sub_w, _), _ = cv2.getTextSize(
                subtitle, cv2.FONT_HERSHEY_SIMPLEX, 0.75, 2
            )
            cv2.putText(
                frame, subtitle, ((w - sub_w) // 2, 178),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                (225, 225, 240), 2, cv2.LINE_AA
            )

            prompt = "CHOOSE YOUR DIFFICULTY"
            (prompt_w, _), _ = cv2.getTextSize(
                prompt, cv2.FONT_HERSHEY_SIMPLEX, 0.72, 2
            )
            cv2.putText(
                frame, prompt, ((w - prompt_w) // 2, 255),
                cv2.FONT_HERSHEY_SIMPLEX, 0.72,
                (245, 245, 255), 2, cv2.LINE_AA
            )

            description = "Select a mode to start your fruit-cutting challenge"
            (desc_w, _), _ = cv2.getTextSize(
                description, cv2.FONT_HERSHEY_SIMPLEX, 0.48, 1
            )
            cv2.putText(
                frame, description, ((w - desc_w) // 2, 286),
                cv2.FONT_HERSHEY_SIMPLEX, 0.48,
                (175, 190, 215), 1, cv2.LINE_AA
            )

            hover_easy = (
                btn_easy[0] <= cx <= btn_easy[2]
                and btn_easy[1] <= cy <= btn_easy[3]
            )
            hover_med = (
                btn_med[0] <= cx <= btn_med[2]
                and btn_med[1] <= cy <= btn_med[3]
            )
            hover_hard = (
                btn_hard[0] <= cx <= btn_hard[2]
                and btn_hard[1] <= cy <= btn_hard[3]
            )
            hover_howto = (
                btn_howto[0] <= cx <= btn_howto[2]
                and btn_howto[1] <= cy <= btn_howto[3]
            )
            hover_settings = (
                btn_settings[0] <= cx <= btn_settings[2]
                and btn_settings[1] <= cy <= btn_settings[3]
            )
            hover_quit = (
                btn_quit[0] <= cx <= btn_quit[2]
                and btn_quit[1] <= cy <= btn_quit[3]
            )

            # Difficulty cards
            mode_cards = [
                (btn_easy, "EASY", "SLOW PACE",
                 (40, 115, 45), hover_easy, selected_difficulty == "EASY"),
                (btn_med, "MEDIUM", "NORMAL PACE",
                 (130, 75, 20), hover_med, selected_difficulty == "MEDIUM"),
                (btn_hard, "HARD", "FAST PACE",
                 (55, 40, 135), hover_hard, selected_difficulty == "HARD"),
            ]

            
            for rect, label, detail, color, hovered, selected in mode_cards:
                x1, y1, x2, y2 = rect

                fill = (
                    tuple(min(255, c + 30) for c in color)
                    if hovered else color
                )

                border = (
                    (0, 0, 255) if selected or hovered
                    else (105, 105, 145)
                )

                draw_rounded_rect(
                    frame,
                    rect,
                    fill,
                    border_color=border,
                    thickness=3 if selected or hovered else 2,
                    radius=18
                )

                (tw, _), _ = cv2.getTextSize(
                    label, cv2.FONT_HERSHEY_DUPLEX, 0.72, 2
                )
                cv2.putText(
                    frame, label,
                    (x1 + (x2 - x1 - tw) // 2, y1 + 31),
                    cv2.FONT_HERSHEY_DUPLEX, 0.72,
                    (255, 255, 255), 2, cv2.LINE_AA
                )

                (dw, _), _ = cv2.getTextSize(
                    detail, cv2.FONT_HERSHEY_SIMPLEX, 0.38, 1
                )
                cv2.putText(
                    frame, detail,
                    (x1 + (x2 - x1 - dw) // 2, y1 + 53),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.38,
                    (215, 220, 235), 1, cv2.LINE_AA
                )


            draw_styled_button(
                frame, btn_howto, "HOW TO PLAY", (70, 65, 105), hover_howto
            )
            draw_styled_button(
                frame, btn_settings, "SETTINGS", (70, 55, 115), hover_settings
            )
            draw_styled_button(
                frame, btn_quit, "QUIT GAME", (95, 42, 55), hover_quit
            )
            # History button
            hover_history = (
                btn_history[0] <= cx <= btn_history[2]
                and btn_history[1] <= cy <= btn_history[3]
            )

            draw_styled_button(
                frame, btn_history, "HISTORY", (45, 85, 125), hover_history
            )

            footer = "Move your index finger and double-touch a button"
            (footer_w, _), _ = cv2.getTextSize(
                footer, cv2.FONT_HERSHEY_SIMPLEX, 0.48, 1
            )
            cv2.putText(
                frame, footer, ((w - footer_w) // 2, h - 52),
                cv2.FONT_HERSHEY_SIMPLEX, 0.48,
                (175, 190, 215), 1, cv2.LINE_AA
            )

            # Choose difficulty and start
            if hover_easy and check_double_click("easy"):
                selected_difficulty = "EASY"
                speed_multiplier = 0.8
                game_state = "PLAYING"

            elif hover_med and check_double_click("med"):
                selected_difficulty = "MEDIUM"
                speed_multiplier = 1.0
                game_state = "PLAYING"

            elif hover_hard and check_double_click("hard"):
                selected_difficulty = "HARD"
                speed_multiplier = 1.35
                game_state = "PLAYING"

            if game_state == "PLAYING":
                score = 0
                lives = 5
                game_record_saved = False
                is_paused = False
                paused_duration = 0
                game_start_time = time.time()

                last_big_bomb_time = time.time()
                last_box_time = time.time()
                last_heart_time = time.time()

                fruit = Fruit(w, h, speed_multiplier)
                extra_fruit = maybe_spawn_extra_fruit(fruit)

                splits.clear()
                boom_effects.clear()
                box_effects.clear()
                heart_effects.clear()
                splashes.clear()

            elif hover_howto and check_double_click("howto"):
                menu_page = "HOW_TO_PLAY"

            elif hover_settings and check_double_click("settings"):
                menu_page = "SETTINGS"

            elif hover_quit and check_double_click("quit"):
                game_state = "QUIT"
            elif hover_history and check_double_click("history"):
                menu_page = "HISTORY"

        # ================= HOW TO PLAY PAGE =================
        
        elif menu_page == "HOW_TO_PLAY":
            title = "HOW TO PLAY"
            (title_w, _), _ = cv2.getTextSize(
                title, cv2.FONT_HERSHEY_DUPLEX, 1.3, 3
            )
            cv2.putText(
                frame, title, ((w - title_w) // 2, 145),
                cv2.FONT_HERSHEY_DUPLEX, 1.3,
                (0, 235, 255), 3, cv2.LINE_AA
            )

            instructions = [
                "1. Show one hand to your webcam.",
                "2. Move your index finger to control the blade.",
                "3. Touch fruits to slice them and earn points.",
                "4. Avoid bombs or you will lose lives.",
                "5. Collect hearts for lives and boxes for bonus points.",
                "6. Use the bottom buttons to go Home, Pause, or Restart."
            ]

            for i, line in enumerate(instructions):
                cv2.putText(
                    frame, line, (panel_left + 45, 225 + i * 48),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.62,
                    (245, 245, 245), 2, cv2.LINE_AA
                )

            hover_back = (
                btn_back[0] <= cx <= btn_back[2]
                and btn_back[1] <= cy <= btn_back[3]
            )
            draw_styled_button(
                frame, btn_back, "< BACK", (70, 55, 115), hover_back
            )

            if hover_back and check_double_click("back_howto"):
                menu_page = "HOME"

        # ================= SETTINGS PAGE =================
        elif menu_page == "SETTINGS":
            btn_back_settings = (
                panel_left + 20, panel_top + 35,
                panel_left + 190, panel_top + 90
            )

            hover_back = (
                btn_back_settings[0] <= cx <= btn_back_settings[2]
                and btn_back_settings[1] <= cy <= btn_back_settings[3]
            )

            # Back button uses the same style as other buttons
            draw_styled_button(
                frame, btn_back_settings, "< BACK",
                (70, 55, 115), hover_back
            )

            title = "SETTINGS"
            (title_w, _), _ = cv2.getTextSize(
                title, cv2.FONT_HERSHEY_DUPLEX, 1.35, 3
            )
            cv2.putText(
                frame, title, ((w - title_w) // 2, 155),
                cv2.FONT_HERSHEY_DUPLEX, 1.35,
                (130, 175, 255), 3, cv2.LINE_AA
            )

            row_x1 = panel_left + 30
            row_x2 = panel_right - 30

            setting_rows = [
                ("sound", "SOUND EFFECTS", sound_effects_enabled, 225),
                ("music", "MUSIC", music_enabled, 295),
                ("vibration", "VIBRATION", vibration_enabled, 365),
            ]

            toggle_rects = {}

            for key_name, label, enabled, row_y in setting_rows:
                cv2.line(
                    frame, (row_x1, row_y + 27),
                    (row_x2, row_y + 27), (48, 48, 72), 1
                )

                cv2.putText(
                    frame, label, (row_x1 + 15, row_y + 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.68,
                    (235, 235, 245), 2, cv2.LINE_AA
                )

                toggle = (
                    row_x2 - 90, row_y - 13,
                    row_x2 - 8, row_y + 18
                )
                toggle_rects[key_name] = toggle

                is_hover = (
                    toggle[0] <= cx <= toggle[2]
                    and toggle[1] <= cy <= toggle[3]
                )

                fill_color = (90, 205, 125) if enabled else (75, 78, 100)
                cv2.rectangle(
                    frame, (toggle[0], toggle[1]),
                    (toggle[2], toggle[3]), fill_color, -1
                )
                cv2.rectangle(
                    frame, (toggle[0], toggle[1]),
                    (toggle[2], toggle[3]),
                    (0, 255, 255) if is_hover else (220, 230, 240), 2
                )

                knob_x = toggle[2] - 16 if enabled else toggle[0] + 16
                cv2.circle(frame, (knob_x, row_y + 2), 12, (250, 250, 250), -1)

                status = "ON" if enabled else "OFF"
                cv2.putText(
                    frame, status, (toggle[0] - 55, row_y + 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                    (130, 235, 165) if enabled else (170, 170, 185),
                    1, cv2.LINE_AA
                )

            cv2.putText(
                frame, "DIFFICULTY LEVEL", (row_x1 + 15, 445),
                cv2.FONT_HERSHEY_SIMPLEX, 0.68,
                (235, 235, 245), 2, cv2.LINE_AA
            )

            diff_y1, diff_y2, diff_gap = 465, 525, 10
            diff_w = (row_x2 - row_x1 - 30 - 2 * diff_gap) // 3

            btn_diff_easy = (
                row_x1 + 15, diff_y1,
                row_x1 + 15 + diff_w, diff_y2
            )
            btn_diff_med = (
                btn_diff_easy[2] + diff_gap, diff_y1,
                btn_diff_easy[2] + diff_gap + diff_w, diff_y2
            )
            btn_diff_hard = (
                btn_diff_med[2] + diff_gap, diff_y1,
                btn_diff_med[2] + diff_gap + diff_w, diff_y2
            )

            difficulty_buttons = [
                ("EASY", btn_diff_easy, (30, 115, 65)),
                ("MEDIUM", btn_diff_med, (35, 85, 145)),
                ("HARD", btn_diff_hard, (95, 45, 65)),
            ]

            for diff_name, rect, color in difficulty_buttons:
                hover = (
                    rect[0] <= cx <= rect[2]
                    and rect[1] <= cy <= rect[3]
                )
                selected = selected_difficulty == diff_name

                draw_styled_button(
                    frame, rect, diff_name, color, hover or selected
                )

                if selected:
                    cv2.rectangle(
                        frame, (rect[0], rect[1]),
                        (rect[2], rect[3]), (120, 220, 165), 2
                    )

            instruction = "Double-touch a switch or difficulty to change it."
            (instruction_w, _), _ = cv2.getTextSize(
                instruction, cv2.FONT_HERSHEY_SIMPLEX, 0.48, 1
            )
            cv2.putText(
                frame, instruction, ((w - instruction_w) // 2, 565),
                cv2.FONT_HERSHEY_SIMPLEX, 0.48,
                (190, 200, 220), 1, cv2.LINE_AA
            )

            # Settings interactions
            if hover_back and check_double_click("back_settings"):
                menu_page = "HOME"

            elif (
                toggle_rects["sound"][0] <= cx <= toggle_rects["sound"][2]
                and toggle_rects["sound"][1] <= cy <= toggle_rects["sound"][3]
                and check_double_click("sound_toggle")
            ):
                sound_effects_enabled = not sound_effects_enabled

            elif (
                toggle_rects["music"][0] <= cx <= toggle_rects["music"][2]
                and toggle_rects["music"][1] <= cy <= toggle_rects["music"][3]
                and check_double_click("music_toggle")
            ):
                music_enabled = not music_enabled
                try:
                    if music_enabled:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()
                except pygame.error:
                    pass

            elif (
                toggle_rects["vibration"][0] <= cx <= toggle_rects["vibration"][2]
                and toggle_rects["vibration"][1] <= cy <= toggle_rects["vibration"][3]
                and check_double_click("vibration_toggle")
            ):
                vibration_enabled = not vibration_enabled

            elif (
                btn_diff_easy[0] <= cx <= btn_diff_easy[2]
                and btn_diff_easy[1] <= cy <= btn_diff_easy[3]
                and check_double_click("settings_easy")
            ):
                selected_difficulty = "EASY"
                speed_multiplier = 0.8

            elif (
                btn_diff_med[0] <= cx <= btn_diff_med[2]
                and btn_diff_med[1] <= cy <= btn_diff_med[3]
                and check_double_click("settings_medium")
            ):
                selected_difficulty = "MEDIUM"
                speed_multiplier = 1.0

            elif (
                btn_diff_hard[0] <= cx <= btn_diff_hard[2]
                and btn_diff_hard[1] <= cy <= btn_diff_hard[3]
                and check_double_click("settings_hard")
            ):
                selected_difficulty = "HARD"
                speed_multiplier = 1.35
        # ================= HISTORY PAGE =================
        elif menu_page == "HISTORY":
            title = "SCORE HISTORY"

            (title_w, _), _ = cv2.getTextSize(
                title, cv2.FONT_HERSHEY_DUPLEX, 1.25, 3
            )

            cv2.putText(
                frame, title, ((w - title_w) // 2, 125),
                cv2.FONT_HERSHEY_DUPLEX, 1.25,
                (0, 235, 255), 3, cv2.LINE_AA
            )

            records = load_score_history()

            if not records:
                message = "No game records yet. Play your first game!"
                (message_w, _), _ = cv2.getTextSize(
                    message, cv2.FONT_HERSHEY_SIMPLEX, 0.65, 2
                )

                cv2.putText(
                    frame, message, ((w - message_w) // 2, 240),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65,
                    (230, 230, 240), 2, cv2.LINE_AA
                )

            else:
                # Table headings
                cv2.putText(
                    frame, "NO.", (170, 175),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55,
                    (0, 255, 255), 2, cv2.LINE_AA
                )

                cv2.putText(
                    frame, "SCORE", (260, 175),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55,
                    (0, 255, 255), 2, cv2.LINE_AA
                )

                cv2.putText(
                    frame, "DIFFICULTY", (420, 175),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55,
                    (0, 255, 255), 2, cv2.LINE_AA
                )

                cv2.putText(
                    frame, "DATE", (650, 175),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55,
                    (0, 255, 255), 2, cv2.LINE_AA
                )

                for index, record in enumerate(records[:10]):
                    row_y = 210 + index * 32

                    cv2.putText(
                        frame, str(index + 1),
                        (175, row_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (240, 240, 240), 1, cv2.LINE_AA
                    )

                    cv2.putText(
                        frame, str(record.get("score", 0)),
                        (260, row_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (100, 255, 130), 2, cv2.LINE_AA
                    )

                    cv2.putText(
                        frame, str(record.get("difficulty", "UNKNOWN")),
                        (420, row_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                        (240, 240, 240), 1, cv2.LINE_AA
                    )

                    date_text = str(record.get("date", "Unknown"))
                    cv2.putText(
                        frame, date_text,
                        (650, row_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                        (220, 220, 235), 1, cv2.LINE_AA
                    )

            # Back button
            hover_back = (
                btn_back[0] <= cx <= btn_back[2]
                and btn_back[1] <= cy <= btn_back[3]
            )

            draw_styled_button(
                frame, btn_back, "< BACK", (70, 55, 115), hover_back
            )

            if hover_back and check_double_click("back_history"):
                menu_page = "HOME"

        if cx != -1 and cy != -1:
            draw_point_cursor(frame, cx, cy)

        show_auto_stretched(window_name, frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q") or key == 27:
            break
        try:
            if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                break
        except cv2.error:
            break
        continue
    if game_state == "GAME_OVER":

        for bx in boom_effects[:]:

            bx.update_and_draw(frame)

            if bx.life <= 0:

                boom_effects.remove(bx)



        cv2.rectangle(frame, (280, 160), (w - 280, 540), (0, 0, 0), -1)

        cv2.rectangle(frame, (280, 160), (w - 280, 540), (0, 0, 255), 3)



        cv2.putText(frame, "GAME OVER!", (w//2 - 150, 230), cv2.FONT_HERSHEY_DUPLEX, 1.5, (0, 0, 255), 3)

        cv2.putText(frame, f"Final Score: {score}", (w//2 - 130, 300), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)



        elapsed = int(end_game_time - game_start_time - paused_duration)

        hrs = elapsed // 3600

        mins = (elapsed % 3600) // 60

        secs = elapsed % 60

        cv2.putText(frame, f"Time Survived: {hrs:02d}:{mins:02d}:{secs:02d}", (w//2 - 180, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)



        restart_btn = (w//2 - 180, 420, w//2 + 180, 490)

        hover_restart = restart_btn[0] <= cx <= restart_btn[2] and restart_btn[1] <= cy <= restart_btn[3]

        draw_styled_button(frame, restart_btn, "RESTART", (0, 160, 240), hover_restart)



        if cx != -1 and cy != -1:

            draw_point_cursor(frame, cx, cy)



        if hover_restart and check_double_click("restart"):

            score = 0

            lives = 5

# Prevent saving the same game more than once
            game_record_saved = False

            game_state = "MENU"



        show_auto_stretched(window_name, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):

            break

        continue



    # ពិនិត្យ Hover លើ Control Buttons

    hover_home = btn_home_rect[0] <= cx <= btn_home_rect[2] and btn_home_rect[1] <= cy <= btn_home_rect[3]

    hover_toggle = btn_toggle_rect[0] <= cx <= btn_toggle_rect[2] and btn_toggle_rect[1] <= cy <= btn_toggle_rect[3]

    hover_ctrl_restart = btn_restart_rect[0] <= cx <= btn_restart_rect[2] and btn_restart_rect[1] <= cy <= btn_restart_rect[3]

    hover_ctrl_bar = hover_home or hover_toggle or hover_ctrl_restart



    # បើមិនទាន់ Pause (មិនទាន់ ឈប់) ទេ ទើបធ្វើការ Update Fruit/Effects

    if not is_paused:

        for sp in splashes[:]:

            sp.update_and_draw(frame)

            if sp.life <= 0:

                splashes.remove(sp)



        fruit.update()

        if fruit.was_reset:

            extra_fruit = maybe_spawn_extra_fruit(fruit)

        fruit.draw(frame)



        if extra_fruit is not None:

            extra_fruit.update()

            extra_fruit.draw(frame)

            if extra_fruit.was_reset:

                extra_fruit = None



        for sp in splits[:]:

            sp.update_and_draw(frame)

            if sp.life <= 0:

                splits.remove(sp)



        for bx in boom_effects[:]:

            bx.update_and_draw(frame)

            if bx.life <= 0:

                boom_effects.remove(bx)



        for box_fx in box_effects[:]:

            box_fx.update_and_draw(frame)

            if box_fx.life <= 0:

                box_effects.remove(box_fx)



        for heart_fx in heart_effects[:]:

            heart_fx.update_and_draw(frame)

            if heart_fx.life <= 0:

                heart_effects.remove(heart_fx)

    else:

        fruit.draw(frame)

        if extra_fruit is not None:

            extra_fruit.draw(frame)

        cv2.putText(frame, "PAUSED", (w//2 - 110, h//2), cv2.FONT_HERSHEY_DUPLEX, 1.8, (0, 255, 255), 3)



    if cx != -1 and cy != -1:

        if hover_ctrl_bar:

            # Pointer នឹងត្រូវគូរម្ដងទៀតនៅខាងក្រោម បន្ទាប់ពី Button

            # ដើម្បីកុំឲ្យ Button បាំង pointer

            pass

        else:

            # Removed jet trail glow behind the shuriken as requested.

            if sword_img is not None:

                overlay_png(frame, sword_img, cx, cy, size=150, angle=-(jet_angle + 90) + shuriken_spin_angle)

            else:

                cv2.circle(frame, (cx, cy), 12, (0, 0, 255), -1)



    # ពិនិត្យការកាប់ផ្លែឈើ

    if cx != -1 and cy != -1 and not is_paused:

        active_fruits = [fruit]

        if extra_fruit is not None:

            active_fruits.append(extra_fruit)



        for target_fruit in active_fruits:

            dist = math.hypot(cx - target_fruit.x, cy - target_fruit.y)

            if dist < target_fruit.radius + 35:

                if target_fruit.is_heart:

                    if lives < 5:

                        lives += 1

                    if surprise_sound:

                        surprise_sound.play()

                    elif slice_sound:

                        slice_sound.play()

                    heart_effects.append(HeartCollectedEffect(target_fruit.x, target_fruit.y))

                elif target_fruit.is_box:

                    score += 200

                    if surprise_sound:

                        surprise_sound.play()

                    elif slice_sound:

                        slice_sound.play()

                    box_effects.append(OpenedBoxEffect(target_fruit.x, target_fruit.y))

                elif target_fruit.is_bomb:

                    if target_fruit.is_big_bomb:

                        lives -= 3

                        if bigboom_sound:

                            bigboom_sound.play()

                        boom_effects.append(BoomExplosion(target_fruit.x, target_fruit.y, is_big=True))

                    else:

                        lives -= 1

                        if boom_sound:

                            boom_sound.play()

                        boom_effects.append(BoomExplosion(target_fruit.x, target_fruit.y, is_big=False))



                    if lives <= 0:

                        lives = 0

                        end_game_time = time.time()

                        game_state = "GAME_OVER"
                        if not game_record_saved:
                            elapsed_seconds = int(
                            end_game_time - game_start_time - paused_duration
                        )

                        record_completed_game(
                            score,
                            selected_difficulty,
                            elapsed_seconds
                        )

                        game_record_saved = True

                else:

                    score += 10

                    if slice_sound:

                        slice_sound.play()



                    splash_color = fruit_splash_map.get(target_fruit.name, "red")

                    splashes.append(JuiceSplash(target_fruit.x, target_fruit.y, splash_color))

                    splits.append(SplitHalf(target_fruit.x, target_fruit.y, target_fruit.img, target_fruit.size))



                if target_fruit is extra_fruit:

                    extra_fruit = None

                else:

                    target_fruit.reset()

                    extra_fruit = maybe_spawn_extra_fruit(target_fruit)



    # ពិនិត្យការចុច Control Buttons

    if hover_home and check_double_click("home"):

        game_state = "MENU"

        is_paused = False

    elif hover_toggle and check_double_click("toggle_pause"):

        is_paused = not is_paused  # ប្តូររវាង Pause និង Play

        if is_paused:

            pause_start_time = time.time()

        else:

            paused_duration += (time.time() - pause_start_time)

    elif hover_ctrl_restart and check_double_click("restart_ctrl"):

        score = 0

        lives = 5

        is_paused = False

        paused_duration = 0

        game_start_time = time.time()

        last_big_bomb_time = time.time()

        last_box_time = time.time()

        last_heart_time = time.time()

        fruit = Fruit(w, h, speed_multiplier)

        extra_fruit = maybe_spawn_extra_fruit(fruit)



    # --- 1. ប្រអប់ SCORE ---

    cv2.rectangle(frame, (20, 20), (320, 80), (0, 0, 0), -1)

    cv2.rectangle(frame, (20, 20), (320, 80), (0, 255, 255), 2)

    cv2.putText(frame, f"SCORE: {score}", (35, 60), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 2)



    # --- 2. ប្រអប់ TIME ---

    if is_paused:

        current_elapsed = int(pause_start_time - game_start_time - paused_duration)

    else:

        current_elapsed = int(time.time() - game_start_time - paused_duration)



    hours = current_elapsed // 3600

    minutes = (current_elapsed % 3600) // 60

    seconds = current_elapsed % 60

    time_str = f"TIME: {hours:02d}:{minutes:02d}:{seconds:02d}"



    cv2.rectangle(frame, (335, 20), (635, 80), (0, 0, 0), -1)

    cv2.rectangle(frame, (335, 20), (635, 80), (0, 255, 255), 2)

    cv2.putText(frame, time_str, (350, 60), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 255, 255), 2)



    # --- 3. ប្រអប់ CONTROL BAR ---

    cv2.rectangle(frame, (ctrl_box_x1, ctrl_box_y1), (ctrl_box_x2, ctrl_box_y2), (0, 0, 0), -1)

    cv2.rectangle(frame, (ctrl_box_x1, ctrl_box_y1), (ctrl_box_x2, ctrl_box_y2), (0, 255, 255), 2)



    
    # Button 1: Home
    draw_rounded_rect(
        frame, btn_home_rect,
        (50, 50, 50) if hover_home else (30, 30, 30),
        border_color=(0, 0, 255),
        thickness=3 if hover_home else 2,
        radius=12
    )

    if home_btn_img is not None:
        overlay_png(
            frame, home_btn_img,
            (btn_home_rect[0] + btn_home_rect[2]) // 2,
            (btn_home_rect[1] + btn_home_rect[3]) // 2,
            size=38
        )

    # Button 2: Pause / Play
    draw_rounded_rect(
        frame, btn_toggle_rect,
        (50, 50, 50) if hover_toggle else (30, 30, 30),
        border_color=(0, 0, 255),
        thickness=3 if hover_toggle else 2,
        radius=12
    )

    current_toggle_icon = stop_btn_img if is_paused else startgame_btn_img

    if current_toggle_icon is not None:
        overlay_png(
            frame, current_toggle_icon,
            (btn_toggle_rect[0] + btn_toggle_rect[2]) // 2,
            (btn_toggle_rect[1] + btn_toggle_rect[3]) // 2,
            size=38
        )

    # Button 3: Restart
    draw_rounded_rect(
        frame, btn_restart_rect,
        (50, 50, 50) if hover_ctrl_restart else (30, 30, 30),
        border_color=(0, 0, 255),
        thickness=3 if hover_ctrl_restart else 2,
        radius=12
    )

    if restart_btn_img is not None:
        overlay_png(
            frame, restart_btn_img,
            (btn_restart_rect[0] + btn_restart_rect[2]) // 2,
            (btn_restart_rect[1] + btn_restart_rect[3]) // 2,
            size=38
        )



    # បង្ហាញ Button 2: startgame.png / stop.png

    # - ពេលលេង (Active/Not Paused): បង្ហាញ startgame.png (ចុចដើម្បី Pause/ឈប់)

    # - ពេលផ្អាក (Paused): បង្ហាញ stop.png (ចុចដើម្បី Start/បន្ត)

    cv2.rectangle(frame, (btn_toggle_rect[0], btn_toggle_rect[1]), (btn_toggle_rect[2], btn_toggle_rect[3]), (50, 50, 50) if hover_toggle else (30, 30, 30), -1)

    cv2.rectangle(frame, (btn_toggle_rect[0], btn_toggle_rect[1]), (btn_toggle_rect[2], btn_toggle_rect[3]), (0, 255, 255) if hover_toggle else (150, 150, 150), 1)



    current_toggle_icon = stop_btn_img if is_paused else startgame_btn_img

    if current_toggle_icon is not None:

        overlay_png(frame, current_toggle_icon, (btn_toggle_rect[0] + btn_toggle_rect[2])//2, (btn_toggle_rect[1] + btn_toggle_rect[3])//2, size=38)



    # បង្ហាញ Button 3: Restart

    cv2.rectangle(frame, (btn_restart_rect[0], btn_restart_rect[1]), (btn_restart_rect[2], btn_restart_rect[3]), (50, 50, 50) if hover_ctrl_restart else (30, 30, 30), -1)

    cv2.rectangle(frame, (btn_restart_rect[0], btn_restart_rect[1]), (btn_restart_rect[2], btn_restart_rect[3]), (0, 255, 255) if hover_ctrl_restart else (150, 150, 150), 1)

    if restart_btn_img is not None:

        overlay_png(frame, restart_btn_img, (btn_restart_rect[0] + btn_restart_rect[2])//2, (btn_restart_rect[1] + btn_restart_rect[3])//2, size=38)



    # បង្ហាញ Pointer លើ Button បន្ទាប់ពីគូរ Button រួច

    # ដើម្បីឲ្យ pointer មើលឃើញច្បាស់ មិនត្រូវបាន Button បាំង

    if cx != -1 and cy != -1 and hover_ctrl_bar:

        draw_point_cursor(frame, cx, cy)



    # បង្ហាញរូបភាពជីវិត/បេះដូង

    for i in range(max(0, lives)):

        life_x = w - 50 - (i * 65)

        life_y = 50

        current_img = life_images[i] if i < len(life_images) else None



        if current_img is not None:

            overlay_png(frame, current_img, life_x, life_y, size=60)

        else:

            cv2.circle(frame, (life_x, life_y), 20, (0, 0, 255), -1)



    show_auto_stretched(window_name, frame)



    if cv2.waitKey(1) & 0xFF == ord('q'):

        break



cap.release()

pygame.mixer.quit()

cv2.destroyAllWindows()
