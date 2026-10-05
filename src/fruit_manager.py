import random
from src.fruit import Fruit

class FruitManager:
    def __init__(self, screen_width=1280, screen_height=720):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fruits = []
        self.spawn_timer = 0
        self.spawn_interval = 45  # Spawns a new wave roughly every 1.5 seconds (at 30 FPS)

    def update(self):
        self.spawn_timer += 1
        
        # Spawn new fruits periodically
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            # Spawn 1 to 3 items per wave
            num_spawns = random.randint(1, 3)
            for _ in range(num_spawns):
                self.fruits.append(Fruit(self.screen_width, self.screen_height))

        # Update physics for each fruit
        for fruit in self.fruits:
            fruit.update()

        # Remove off-screen fruits to optimize memory & performance
        self.fruits = [f for f in self.fruits if not f.is_off_screen()]

    def draw(self, frame):
        # Draw all active fruits
        for fruit in self.fruits:
            fruit.draw(frame)