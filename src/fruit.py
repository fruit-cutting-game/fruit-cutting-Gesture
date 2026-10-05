import cv2
import random
import os

class Fruit:
    _image_cache = {}

    def __init__(self, screen_width=1280, screen_height=720):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # 1. Fruit Types and Asset Definitions
        self.fruit_types = [
    {'name': 'watermelon', 'path': 'assets/fruits/watermelon.png', 'color': (0, 200, 0), 'is_bomb': False},
    {'name': 'apple',      'path': 'assets/fruits/apple.png',      'color': (0, 0, 220), 'is_bomb': False},
    {'name': 'orange',     'path': 'assets/fruits/orange.png',     'color': (0, 140, 255), 'is_bomb': False},
    {'name': 'banana',     'path': 'assets/fruits/banana.png',     'color': (0, 230, 255), 'is_bomb': False},
    {'name': 'bomb',       'path': 'assets/fruits/bomb.png',       'color': (50, 50, 50), 'is_bomb': True}
]
    

        # 80% chance for regular fruit, 20% chance for bomb
        if random.random() < 0.2:
            self.type_data = self.fruit_types[-1] # Bomb
        else:
            self.type_data = random.choice(self.fruit_types[:-1]) # Random Fruit

        self.is_bomb = self.type_data['is_bomb']
        self.radius = 50  # Size of fruit collision radius

        # 2. Physics Setup
        self.x = random.randint(150, screen_width - 150)
        self.y = screen_height + 60
        self.velocity_x = random.choice([-5, -3, -1, 1, 3, 5])
        self.velocity_y = random.randint(-22, -16)
        self.gravity = 0.6
        self.is_sliced = False

        # 3. Load & Cache Image Asset
        self.image = self._load_image(self.type_data['path'], size=(self.radius * 2, self.radius * 2))

    def _load_image(self, path, size):
        if path in Fruit._image_cache:
            return Fruit._image_cache[path]

        if os.path.exists(path):
            img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
            if img is not None:
                img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
                Fruit._image_cache[path] = img
                return img
        return None

    def update(self):
        # Physics update step
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_y += self.gravity

    def draw(self, frame):
        if self.is_sliced:
            return

        ix, iy = int(self.x), int(self.y)

        # Render transparent PNG image over camera frame
        if self.image is not None:
            self._overlay_png(frame, self.image, ix, iy)
        else:
            # Color circle fallback if image is missing
            cv2.circle(frame, (ix, iy), self.radius, self.type_data['color'], -1)
            cv2.circle(frame, (ix, iy), self.radius, (255, 255, 255), 2)

    def _overlay_png(self, frame, img_png, cx, cy):
        """Alpha blending function to overlay transparent 4-channel PNG onto 3-channel frame."""
        h, w, c = img_png.shape
        x1, y1 = cx - w // 2, cy - h // 2
        x2, y2 = x1 + w, y1 + h

        # Prevent index out of bounds error near frame borders
        if x1 < 0 or y1 < 0 or x2 > self.screen_width or y2 > self.screen_height:
            return

        # Check if image has alpha channel (transparency)
        if img_png.shape[2] == 4:
            alpha_png = img_png[:, :, 3] / 255.0
            alpha_frame = 1.0 - alpha_png

            for ch in range(0, 3):
                frame[y1:y2, x1:x2, ch] = (
                    alpha_png * img_png[:, :, ch] + alpha_frame * frame[y1:y2, x1:x2, ch]
                )
        else:
            frame[y1:y2, x1:x2] = img_png[:, :, :3]

    def is_off_screen(self):
        return self.y > self.screen_height + 100