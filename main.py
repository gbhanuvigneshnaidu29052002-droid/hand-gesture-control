"""
Hand Gesture Control System - Main Entry Point
Author: Bhanu Vignesh Naidu Ganeshna
Description: Real-time touchless UI & mouse controller powered by MediaPipe and OpenCV.
"""

import sys
import os

# Add workspace directory to python path for modular importability
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.hand_detector import HandDetector
from src.gesture_controller import GestureController
from src.mouse_controller import MouseController
import config
import cv2
import time
import numpy as np

def run_controller(cam_id=0, draw_hud=True):
    """
    Executes high-performance non-blocking webcam processing loop (20-30+ FPS).
    """
    cap = cv2.VideoCapture(cam_id)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAM_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAM_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    detector = HandDetector(
        max_hands=config.MAX_HANDS,
        model_complexity=config.MODEL_COMPLEXITY,
        detection_conf=config.DETECTION_CONFIDENCE,
        tracking_conf=config.TRACKING_CONFIDENCE
    )
    gesture_ctrl = GestureController()
    mouse_ctrl = MouseController(smoothening=config.SMOOTHENING)
    
    prev_time = time.time()
    last_click_time = 0
    last_scroll_time = 0
    prev_palm_y = None

    print("🚀 Hand Gesture Control Running (20-30+ FPS Mode). Press 'q' to exit.")
    print("🖐️  Supported Gestures:")
    print("   - POINT (Index up): Move Cursor")
    print("   - DRAG (Pinch Thumb to Index): Drag & Drop")
    print("   - CLICK (Index+Middle): Single Left Click")
    print("   - DOUBLE_CLICK (Index+Middle+Ring): Double Click")
    print("   - RIGHT_CLICK (Index+Pinky): Right Click")
    print("   - PALM_SCROLL (Open Palm): Move Open Palm UP/DOWN to scroll gently")
    
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("⚠️ Failed to capture camera frame.")
            break
            
        # Mirror image for intuitive control
        frame = cv2.flip(frame, 1)
        
        # Detect hands
        frame = detector.find_hands(frame, draw=draw_hud)
        landmarks = detector.get_landmarks(frame)
        
        # Bounding box / Control area visualization
        if draw_hud:
            cv2.rectangle(
                frame,
                (config.FRAME_REDUCTION, config.FRAME_REDUCTION),
                (config.CAM_WIDTH - config.FRAME_REDUCTION, config.CAM_HEIGHT - config.FRAME_REDUCTION),
                (255, 0, 255), 2
            )

        hud_gesture_text = "NONE"

        if landmarks:
            # Index finger tip coordinate (landmark 8) and Palm center (landmark 9)
            index_x, index_y = landmarks[8][1], landmarks[8][2]
            palm_y = landmarks[9][2]
            
            # Calculate pinch distance (Thumb 4 to Index 8)
            pinch_dist, frame, _ = detector.find_distance(4, 8, frame, draw=False)
            fingers = detector.fingers_up()
            gesture = gesture_ctrl.detect_gesture(fingers, pinch_distance=pinch_dist)
            hud_gesture_text = gesture

            curr_timestamp = time.time()

            # Non-blocking Action Dispatching
            if gesture == "POINT":
                prev_palm_y = None
                mouse_ctrl.stop_drag()
                mouse_ctrl.move(index_x, index_y, config.FRAME_REDUCTION, config.CAM_WIDTH, config.CAM_HEIGHT)
                cv2.circle(frame, (index_x, index_y), 10, (0, 255, 0), cv2.FILLED)

            elif gesture == "CLICK":
                prev_palm_y = None
                mouse_ctrl.stop_drag()
                if curr_timestamp - last_click_time > config.CLICK_DELAY:
                    mouse_ctrl.click()
                    last_click_time = curr_timestamp
                cv2.circle(frame, (index_x, index_y), 14, (0, 0, 255), cv2.FILLED)

            elif gesture == "DOUBLE_CLICK":
                prev_palm_y = None
                mouse_ctrl.stop_drag()
                if curr_timestamp - last_click_time > config.CLICK_DELAY:
                    mouse_ctrl.double_click()
                    last_click_time = curr_timestamp
                cv2.circle(frame, (index_x, index_y), 16, (255, 0, 255), cv2.FILLED)

            elif gesture == "RIGHT_CLICK":
                prev_palm_y = None
                mouse_ctrl.stop_drag()
                if curr_timestamp - last_click_time > config.CLICK_DELAY:
                    mouse_ctrl.right_click()
                    last_click_time = curr_timestamp
                cv2.circle(frame, (index_x, index_y), 14, (255, 255, 0), cv2.FILLED)

            elif gesture == "PALM_SCROLL":
                mouse_ctrl.stop_drag()
                if prev_palm_y is not None:
                    delta_y = palm_y - prev_palm_y
                    if curr_timestamp - last_scroll_time > config.SCROLL_COOLDOWN:
                        if delta_y < -config.SCROLL_DEADZONE: # Moving Palm UP
                            scroll_amount = int(min(50, max(10, abs(delta_y) * config.SCROLL_SENSITIVITY)))
                            mouse_ctrl.scroll_up(scroll_amount)
                            last_scroll_time = curr_timestamp
                            hud_gesture_text = f"SCROLL UP (Palm ^ {scroll_amount})"
                        elif delta_y > config.SCROLL_DEADZONE: # Moving Palm DOWN
                            scroll_amount = int(min(50, max(10, abs(delta_y) * config.SCROLL_SENSITIVITY)))
                            mouse_ctrl.scroll_down(scroll_amount)
                            last_scroll_time = curr_timestamp
                            hud_gesture_text = f"SCROLL DOWN (Palm v {scroll_amount})"
                        else:
                            hud_gesture_text = "PALM SCROLL (Hold / Move UP/DOWN)"
                prev_palm_y = palm_y
                cv2.circle(frame, (landmarks[9][1], palm_y), 12, (255, 128, 0), cv2.FILLED)

            elif gesture == "DRAG":
                prev_palm_y = None
                mouse_ctrl.start_drag()
                mouse_ctrl.move(index_x, index_y, config.FRAME_REDUCTION, config.CAM_WIDTH, config.CAM_HEIGHT)
                cv2.circle(frame, (index_x, index_y), 14, (0, 165, 255), cv2.FILLED)
            else:
                prev_palm_y = None
                mouse_ctrl.stop_drag()

            # HUD Feedback
            if draw_hud:
                cv2.putText(frame, f"Gesture: {hud_gesture_text}", (20, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        else:
            prev_palm_y = None
            mouse_ctrl.stop_drag()

        # Calculate & Display FPS
        curr_time = time.time()
        fps = 1.0 / (curr_time - prev_time + 1e-6)
        prev_time = curr_time
        
        if draw_hud:
            color = (0, 255, 0) if fps >= 20 else (0, 165, 255)
            cv2.putText(frame, f"FPS: {int(fps)}", (config.CAM_WIDTH - 140, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
                        
        cv2.imshow("Hand Gesture Control (High FPS)", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    mouse_ctrl.stop_drag()
    cap.release()
    cv2.destroyAllWindows()
    print("👋 Controller terminated cleanly.")

if __name__ == "__main__":
    run_controller()
