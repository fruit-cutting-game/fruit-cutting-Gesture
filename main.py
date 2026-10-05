import cv2
from src.camera import CameraManager
from src.hand_tracker import HandTracker
from src.blade import BladeTrail
from src.fruit_manager import FruitManager  # <-- New import

def main():
    # 1. Initialize all managers (Week 1 + Week 2)
    camera = CameraManager()
    tracker = HandTracker()
    blade = BladeTrail()
    fruit_manager = FruitManager()  # <-- New instance

    window_name = "Gesture Fruit Cutter - Week 2 Test"

    while True:
        frame = camera.get_frame()
        if frame is None:
            break

        # 2. Track finger and update blade trail (Week 1 code)
        finger_tip = tracker.get_index_tip(frame)
        blade.update(finger_tip)

        # 3. Update physics & draw fruits on the screen (Week 2 code)
        fruit_manager.update()
        fruit_manager.draw(frame)

        # 4. Draw the blade trail on top of the fruits
        blade.draw(frame)

        # 5. Render final frame on display
        cv2.imshow(window_name, frame)

        # Exit conditions
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()