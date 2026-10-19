"""Basic circle collision utilities."""
import math

def point_hits_circle(point, center, radius):
    return math.hypot(point[0]-center[0], point[1]-center[1]) <= radius
