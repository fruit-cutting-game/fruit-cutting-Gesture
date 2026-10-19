"""Fruit model used by modular game logic."""
from dataclasses import dataclass
@dataclass
class Fruit:
    x: float
    y: float
    radius: float = 30
    points: int = 10
    kind: str = "apple"
    sliced: bool = False
