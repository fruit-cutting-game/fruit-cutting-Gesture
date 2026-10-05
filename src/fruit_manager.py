import random
from src.fruit import Fruit

class FruitManager:
    def __init__(self, screen_width=1280, screen_height=720):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fruits = []
        self.spawn_timer = 0
        self.spawn_interval = 40  # Spawns new wave every ~1.3 seconds

    def update(self):
        self.spawn_timer += 1
        
        # Spawn wave
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            num_spawns = random.randint(1, 3)
            for _ in range(num_spawns):
                self.fruits.append(Fruit(self.screen_width, self.screen_height))

        # Update physics positions
        for fruit in self.fruits:
            fruit.update()

        # Remove off-screen objects
        self.fruits = [f for f in self.fruits if not f.is_off_screen()]

    def draw(self, frame):
        for fruit in self.fruits:
            fruit.draw(frame)