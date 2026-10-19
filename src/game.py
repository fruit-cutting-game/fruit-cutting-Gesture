import cv2
import mediapipe as mp
import random
import math
import os
import collections
import time
import pygame
import numpy as np

# 0. Initialize Pygame Mixer for Audio
pygame.mixer.init()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSET_FOLDER = os.path.join(BASE_DIR, "assets")
SOUND_FOLDER = os.path.join(ASSET_FOLDER, "sounds")

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
    "watermelon": "watermelon.png"
}

fruit_images = {}
for name, filename in fruit_files.items():
    path = os.path.join(IMAGE_FOLDER, filename)
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if img is not None:
        fruit_images[name] = img

splash_images = {
    "yellow": cv2.imread(os.path.join(IMAGE_FOLDER, "yellow.png"), cv2.IMREAD_UNCHANGED),
    "red": cv2.imread(os.path.join(IMAGE_FOLDER, "red.png"), cv2.IMREAD_UNCHANGED),
    "blue": cv2.imread(os.path.join(IMAGE_FOLDER, "blue.png"), cv2.IMREAD_UNCHANGED)
}

fruit_splash_map = {
    "orange": "yellow",
    "pineapple": "yellow",
    "banana": "yellow",
    "apple": "red",
    "watermelon": "red",
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
    if random.random() >= 0.45:
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

def draw_styled_button(frame, rect, text, base_color, is_hover=False):
    x1, y1, x2, y2 = rect
    font = cv2.FONT_HERSHEY_DUPLEX

    if is_hover:
        x1 -= 8
        y1 -= 4
        x2 += 8
        y2 += 4
        hover_bg = tuple(min(255, c + 50) for c in base_color)
        cv2.rectangle(frame, (x1, y1), (x2, y2), hover_bg, -1)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 4)
        scale = 0.95
        thickness = 2
        text_color = (0, 255, 255)
    else:
        cv2.rectangle(frame, (x1, y1), (x2, y2), base_color, -1)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (220, 220, 220), 2)
        scale = 0.85
        thickness = 2
        text_color = (255, 255, 255)

    (text_w, text_h), _ = cv2.getTextSize(text, font, scale, thickness)
    text_x = x1 + (x2 - x1 - text_w) // 2
    text_y = y1 + (y2 - y1 + text_h) // 2

    cv2.putText(frame, text, (text_x + 2, text_y + 2), font, scale, (0, 0, 0), thickness + 1)
    cv2.putText(frame, text, (text_x, text_y), font, scale, text_color, thickness)

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

game_state = "MENU"
speed_multiplier = 1.0

score = 0
lives = 5
fruit = Fruit(w, h, speed_multiplier)
extra_fruit = None
splits = []
boom_effects = []
box_effects = []
heart_effects = []
splashes = []
finger_trail = collections.deque(maxlen=12)

jet_angle = -90
shuriken_spin_angle = 0  # Extra rotation for the shuriken

btn_easy = (w//2 - 200, 280, w//2 + 200, 340)
btn_med  = (w//2 - 200, 370, w//2 + 200, 430)
btn_hard = (w//2 - 200, 460, w//2 + 200, 520)

ctrl_box_x1, ctrl_box_y1 = 20, h - 90
ctrl_box_x2, ctrl_box_y2 = 230, h - 20

btn_home_rect = (30, h - 80, 85, h - 30)
btn_toggle_rect = (97, h - 80, 152, h - 30)  # ប្រអប់ប៊ូតុងកណ្តាល (សម្រាប់ startgame.png / stop.png)
btn_restart_rect = (165, h - 80, 220, h - 30)

while True:
    # Rotate the shuriken continuously (degrees per frame).
    shuriken_spin_angle = (shuriken_spin_angle + 12) % 360

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

    if game_state == "MENU":
        cv2.rectangle(frame, (250, 100), (w - 250, 620), (0, 0, 0), -1)
        cv2.rectangle(frame, (250, 100), (w - 250, 620), (0, 255, 255), 3)

        cv2.putText(frame, "FRUIT NINJA GAME", (w//2 - 210, 175), cv2.FONT_HERSHEY_DUPLEX, 1.4, (0, 255, 255), 3)
        cv2.putText(frame, "Double touch button to start:", (w//2 - 200, 225), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        hover_easy = btn_easy[0] <= cx <= btn_easy[2] and btn_easy[1] <= cy <= btn_easy[3]
        hover_med  = btn_med[0] <= cx <= btn_med[2] and btn_med[1] <= cy <= btn_med[3]
        hover_hard = btn_hard[0] <= cx <= btn_hard[2] and btn_hard[1] <= cy <= btn_hard[3]

        draw_styled_button(frame, btn_easy, "EASY MODE", (0, 160, 0), hover_easy)
        draw_styled_button(frame, btn_med, "MEDIUM MODE", (0, 120, 240), hover_med)
        draw_styled_button(frame, btn_hard, "HARD MODE", (0, 0, 200), hover_hard)

        if cx != -1 and cy != -1:
            draw_point_cursor(frame, cx, cy)

        if hover_easy and check_double_click("easy"):
            speed_multiplier = 0.8
            game_state = "PLAYING"
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
        elif hover_med and check_double_click("med"):
            speed_multiplier = 1.0
            game_state = "PLAYING"
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
        elif hover_hard and check_double_click("hard"):
            speed_multiplier = 1.35
            game_state = "PLAYING"
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

        show_auto_stretched(window_name, frame)

        key = cv2.waitKey(1) & 0xFF

# Close the game by pressing Q or Esc
        if key == ord('q') or key == 27:
            break

# Close the game when clicking the X button
        try:
            if cv2.getWindowProperty(
        window_name, cv2.WND_PROP_VISIBLE) < 1:
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

    # បង្ហាញ Button 1: Home
    cv2.rectangle(frame, (btn_home_rect[0], btn_home_rect[1]), (btn_home_rect[2], btn_home_rect[3]), (50, 50, 50) if hover_home else (30, 30, 30), -1)
    cv2.rectangle(frame, (btn_home_rect[0], btn_home_rect[1]), (btn_home_rect[2], btn_home_rect[3]), (0, 255, 255) if hover_home else (150, 150, 150), 1)
    if home_btn_img is not None:
        overlay_png(frame, home_btn_img, (btn_home_rect[0] + btn_home_rect[2])//2, (btn_home_rect[1] + btn_home_rect[3])//2, size=38)

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