import cv2
import mediapipe as mp
import os

class HandTracker:
    def __init__(self, model_path='hand_landmarker.task'):
        # ពិនិត្យមើលថាមាន File Model ឬនៅ
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"រកមិនឃើញ File '{model_path}' ទេ។ សូម Download វាដាក់ក្នុង Folder គម្រោងជាមុនសិន!")

        # ប្រើប្រាស់ Tasks API ផ្លូវការថ្មីរបស់ MediaPipe
        BaseOptions = mp.tasks.BaseOptions
        HandLandmarker = mp.tasks.vision.HandLandmarker
        HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode

        options = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=VisionRunningMode.IMAGE,
            num_hands=1
        )
        self.landmarker = HandLandmarker.create_from_options(options)

    def get_index_tip(self, frame):
        h, w, _ = frame.shape
        # បំប្លែង BGR Frame ទៅជា MediaPipe Image Format
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        # ចាប់យក Hand Landmarks
        results = self.landmarker.detect(mp_image)

        if results.hand_landmarks:
            for hand_landmarks in results.hand_landmarks:
                # Landmark 8 គឺជា Index Finger Tip (ចុងម្រាមដៃចង្អុល)
                index_tip = hand_landmarks[8]
                return int(index_tip.x * w), int(index_tip.y * h)
        return None