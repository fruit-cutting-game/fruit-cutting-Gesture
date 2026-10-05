import cv2

class CameraManager:
    def __init__(self, width=1280, height=720):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def get_frame(self):
        success, frame = self.cap.read()
        if not success:
            return None
        # ឆ្លុះកញ្ចក់ (Horizontal Flip)
        return cv2.flip(frame, 1)

    def release(self):
        self.cap.release()