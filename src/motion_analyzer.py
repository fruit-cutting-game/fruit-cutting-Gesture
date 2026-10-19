"""Helpers for measuring hand movement."""
import math

def distance(a, b):
    return math.hypot(b[0]-a[0], b[1]-a[1])

def speed(a, b, elapsed_seconds):
    return distance(a, b) / max(elapsed_seconds, 1e-6)
