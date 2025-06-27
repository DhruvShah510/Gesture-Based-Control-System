# utils.py

import math

def calculate_distance(p1, p2):
    """Calculate Euclidean distance between two (x, y) points."""
    x1, y1 = p1
    x2, y2 = p2
    return math.hypot(x2 - x1, y2 - y1)
