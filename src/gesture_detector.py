"""Configurable cutting-gesture detection."""
from .motion_analyzer import distance, speed

def is_cut(previous, current, elapsed_seconds, min_distance=25, min_speed=180):
    return distance(previous, current) >= min_distance and speed(previous, current, elapsed_seconds) >= min_speed
