import cv2
import time

from src.hand_detector import HandDetector
from src.gesture_controller import GestureController
from src.mouse_controller import MouseController
import config

def main():
    # Initialize camera
    cap = cv2.VideoCapture(0)
    cap.set(3, config.CAMERA_WIDTH)
    cap.set(4, config.CAMERA_HEIGHT)

    # Initialize modules
    detector = HandDetector()
    gesture_ctrl = GestureController()
    mouse = MouseController(config.SMOOTHENING)

    prev_time = 0
    last_click_time = 0

    while True:
        success, frame = cap.read()
        if not success:
            break

        # Flip frame for mirror effect
        frame = cv2.flip(frame, 1)

        # Detect hands
        frame = detector.find_hands(frame)
        landmarks = detector.get_landmarks(frame)
        fingers = detector.fingers_up()

        # Detect gesture
        gesture = gesture_ctrl.detect_gesture(fingers)

        # If hand detected
        if landmarks:
            x, y = landmarks[8][1], landmarks[8][2]

            if gesture == "POINT":
                mouse.move(
                    x, y,
                    config.FRAME_REDUCTION,
                    config.CAMERA_WIDTH,
                    config.CAMERA_HEIGHT
                )

            elif gesture == "CLICK" and time.time() - last_click_time > config.CLICK_DELAY:
                mouse.click()
                last_click_time = time.time()

            elif gesture == "DOUBLE_CLICK" and time.time() - last_click_time > config.CLICK_DELAY:
                mouse.double_click()
                last_click_time = time.time()

        # FPS calculation
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if prev_time else 0
        prev_time = curr_time

        # Display FPS
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        cv2.imshow("Gesture Control", frame)

        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()