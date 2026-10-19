"""Fruit collection and spawning helpers."""
import random
class FruitManager:
    def __init__(self): self.fruits = []
    def add(self, fruit): self.fruits.append(fruit)
    def remove(self, fruit):
        if fruit in self.fruits: self.fruits.remove(fruit)
    def random_x(self, width, margin=40): return random.randint(margin, max(margin, width-margin))
