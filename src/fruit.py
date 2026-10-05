import cv2
import random

class Fruit:
    def __init__(self, screen_width=1280, screen_height=720):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # 1. Randomize launch positions at the bottom of the screen
        self.x = random.randint(100, screen_width - 100)
        self.y = screen_height + 50  # Start slightly below the bottom edge
        
        # 2. Randomize launch speed and upward angle
        self.velocity_x = random.choice([-5, -3, -2, 2, 3, 5])
        self.velocity_y = random.randint(-22, -16)  # Negative speed launches upwards
        
        # 3. Physics parameters
        self.gravity = 0.6
        self.radius = 40
        self.is_sliced = False
        
        # 4. Item types (80% chance Fruit, 20% chance Bomb)
        self.is_bomb = random.random() < 0.2
        if self.is_bomb:
            self.color = (0, 0, 255)  # Red for bomb
        else:
            self.color = random.choice([
                (0, 255, 0),    # Green (Watermelon)
                (0, 165, 255),  # Orange
                (0, 255, 255)   # Yellow (Banana/Lemon)
            ])

    def update(self):
        # Apply physics motion
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_y += self.gravity  # Gravity pulls it down continuously

    def draw(self, frame):
        # Draw fruit/bomb as a colored circle on the frame
        if not self.is_sliced:
            cv2.circle(frame, (int(self.x), int(self.y)), self.radius, self.color, -1)
            # Draw an inner core line for visual depth
            cv2.circle(frame, (int(self.x), int(self.y)), self.radius, (255, 255, 255), 2)

    def is_off_screen(self):
        # Check if the fruit has fallen back below the screen bottom
        return self.y > self.screen_height + 100