"""Webcam setup helpers."""
import cv2

def open_camera(index=0, width=None, height=None):
    """Open webcam and optionally request a resolution. Returns VideoCapture."""
    camera = cv2.VideoCapture(index)
    if width: camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    if height: camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    return camera
