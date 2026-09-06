"""
Automated Unit Test Suite for Real-Time Hand Gesture Control System
Author: Bhanu Vignesh Naidu Ganeshna
"""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch
import numpy as np

# Add project root to Python search path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import config
from src.gesture_controller import GestureController
from src.mouse_controller import MouseController
from src.hand_detector import HandDetector


class TestConfig(unittest.TestCase):
    """Verifies configuration parameters, resolution geometry, and thresholds."""

    def test_camera_dimensions(self):
        self.assertGreater(config.CAM_WIDTH, 0)
        self.assertGreater(config.CAM_HEIGHT, 0)
        self.assertEqual(config.CAM_WIDTH, config.CAMERA_WIDTH)
        self.assertEqual(config.CAM_HEIGHT, config.CAMERA_HEIGHT)

    def test_performance_hyperparameters(self):
        self.assertGreaterEqual(config.MAX_HANDS, 1)
        self.assertIn(config.MODEL_COMPLEXITY, [0, 1, 2])
        self.assertGreater(config.DETECTION_CONFIDENCE, 0.0)
        self.assertLessEqual(config.DETECTION_CONFIDENCE, 1.0)
        self.assertGreater(config.TRACKING_CONFIDENCE, 0.0)
        self.assertLessEqual(config.TRACKING_CONFIDENCE, 1.0)

    def test_control_thresholds(self):
        self.assertGreater(config.FRAME_REDUCTION, 0)
        self.assertGreaterEqual(config.SMOOTHENING, 1)
        self.assertGreater(config.PINCH_THRESHOLD, 0)
        self.assertGreaterEqual(config.BUFFER_SIZE, 2)
        self.assertGreater(config.CLICK_DELAY, 0.0)
        self.assertGreater(config.SCROLL_SPEED, 0)
        self.assertGreater(config.SCROLL_SENSITIVITY, 0.0)


class TestGestureController(unittest.TestCase):
    """Validates kinematic gesture classification and temporal hysteresis filtering."""

    def setUp(self):
        self.controller = GestureController(buffer_size=4)

    def test_point_gesture(self):
        # Index UP only: [Thumb, Index, Middle, Ring, Pinky]
        fingers = [False, True, False, False, False]
        # First frame appends to buffer
        self.controller.detect_gesture(fingers, pinch_distance=100)
        # Second consecutive frame triggers threshold count >= 2
        gesture = self.controller.detect_gesture(fingers, pinch_distance=100)
        self.assertEqual(gesture, "POINT")

    def test_drag_gesture_via_pinch(self):
        # Pinch distance below threshold triggers DRAG regardless of finger booleans
        fingers = [True, True, False, False, False]
        pinch_distance = config.PINCH_THRESHOLD - 5
        self.controller.detect_gesture(fingers, pinch_distance=pinch_distance)
        gesture = self.controller.detect_gesture(fingers, pinch_distance=pinch_distance)
        self.assertEqual(gesture, "DRAG")

    def test_click_gesture(self):
        # Index + Middle UP: [Thumb, Index, Middle, Ring, Pinky]
        fingers = [False, True, True, False, False]
        self.controller.detect_gesture(fingers, pinch_distance=100)
        gesture = self.controller.detect_gesture(fingers, pinch_distance=100)
        self.assertEqual(gesture, "CLICK")

    def test_double_click_gesture(self):
        # Index + Middle + Ring UP
        fingers = [False, True, True, True, False]
        self.controller.detect_gesture(fingers, pinch_distance=100)
        gesture = self.controller.detect_gesture(fingers, pinch_distance=100)
        self.assertEqual(gesture, "DOUBLE_CLICK")

    def test_right_click_gesture(self):
        # Index + Pinky UP
        fingers_index_pinky = [False, True, False, False, True]
        self.controller.detect_gesture(fingers_index_pinky, pinch_distance=100)
        gesture = self.controller.detect_gesture(fingers_index_pinky, pinch_distance=100)
        self.assertEqual(gesture, "RIGHT_CLICK")

        # Pinky only UP
        controller2 = GestureController(buffer_size=4)
        fingers_pinky_only = [False, False, False, False, True]
        controller2.detect_gesture(fingers_pinky_only, pinch_distance=100)
        gesture2 = controller2.detect_gesture(fingers_pinky_only, pinch_distance=100)
        self.assertEqual(gesture2, "RIGHT_CLICK")

    def test_palm_scroll_gesture(self):
        # Open Palm: all 4 fingers extended
        fingers = [True, True, True, True, True]
        self.controller.detect_gesture(fingers, pinch_distance=100)
        gesture = self.controller.detect_gesture(fingers, pinch_distance=100)
        self.assertEqual(gesture, "PALM_SCROLL")

    def test_unrecognized_gesture_none(self):
        # Fist: all fingers folded
        fingers = [False, False, False, False, False]
        self.controller.detect_gesture(fingers, pinch_distance=100)
        gesture = self.controller.detect_gesture(fingers, pinch_distance=100)
        self.assertEqual(gesture, "NONE")

    def test_temporal_hysteresis_resists_single_frame_noise(self):
        # Stabilize on POINT
        point_fingers = [False, True, False, False, False]
        self.controller.detect_gesture(point_fingers, pinch_distance=100)
        stable = self.controller.detect_gesture(point_fingers, pinch_distance=100)
        self.assertEqual(stable, "POINT")

        # Inject single frame of random transient noise (e.g., CLICK)
        transient_click = [False, True, True, False, False]
        filtered = self.controller.detect_gesture(transient_click, pinch_distance=100)
        # Should stay on POINT because count for CLICK is only 1 (< 2)
        self.assertEqual(filtered, "POINT")


class TestMouseController(unittest.TestCase):
    """Validates cursor kinematics, exponential smoothing, and event dispatching."""

    @patch('src.mouse_controller.pyautogui')
    def test_initialization(self, mock_pyautogui):
        mock_pyautogui.size.return_value = (1920, 1080)
        mouse = MouseController(smoothening=5)
        self.assertEqual(mouse.smoothening, 5)
        self.assertEqual(mouse.screen_w, 1920)
        self.assertEqual(mouse.screen_h, 1080)
        self.assertFalse(mouse.is_dragging)

    @patch('src.mouse_controller.pyautogui')
    def test_cursor_move_and_exponential_smoothing(self, mock_pyautogui):
        mock_pyautogui.size.return_value = (1920, 1080)
        mouse = MouseController(smoothening=5)
        mouse.prev_x, mouse.prev_y = 100.0, 100.0

        # Move with cam coordinate in center
        mouse.move(x=320, y=240, frame_reduction=80, cam_w=640, cam_h=480)
        mock_pyautogui.moveTo.assert_called_once()
        call_x, call_y = mock_pyautogui.moveTo.call_args[0]
        # Target coordinate is screen midpoint (960, 540)
        # Smoothed pos: prev + (target - prev) / 5 = 100 + (960 - 100)/5 = 272.0
        self.assertAlmostEqual(call_x, 272.0, places=1)
        self.assertAlmostEqual(call_y, 188.0, places=1)

    @patch('src.mouse_controller.pyautogui')
    def test_click_actions(self, mock_pyautogui):
        mock_pyautogui.size.return_value = (1920, 1080)
        mouse = MouseController()

        mouse.click()
        mock_pyautogui.click.assert_called_once_with(_pause=False)

        mouse.double_click()
        mock_pyautogui.doubleClick.assert_called_once_with(_pause=False)

        mouse.right_click()
        mock_pyautogui.rightClick.assert_called_once_with(_pause=False)

    @patch('src.mouse_controller.pyautogui')
    def test_scroll_actions(self, mock_pyautogui):
        mock_pyautogui.size.return_value = (1920, 1080)
        mouse = MouseController()

        mouse.scroll_up(amount=30)
        mock_pyautogui.scroll.assert_called_with(30, _pause=False)

        mouse.scroll_down(amount=30)
        mock_pyautogui.scroll.assert_called_with(-30, _pause=False)

    @patch('src.mouse_controller.pyautogui')
    def test_drag_and_drop_state(self, mock_pyautogui):
        mock_pyautogui.size.return_value = (1920, 1080)
        mouse = MouseController()

        # Start drag
        mouse.start_drag()
        self.assertTrue(mouse.is_dragging)
        mock_pyautogui.mouseDown.assert_called_once_with(_pause=False)

        # Repeated start_drag should not call mouseDown again
        mouse.start_drag()
        self.assertEqual(mock_pyautogui.mouseDown.call_count, 1)

        # Stop drag
        mouse.stop_drag()
        self.assertFalse(mouse.is_dragging)
        mock_pyautogui.mouseUp.assert_called_once_with(_pause=False)


class TestHandDetector(unittest.TestCase):
    """Validates MediaPipe landmark extraction, distance measuring, and finger parsing."""

    def setUp(self):
        self.detector = HandDetector(
            max_hands=config.MAX_HANDS,
            model_complexity=config.MODEL_COMPLEXITY,
            detection_conf=config.DETECTION_CONFIDENCE,
            tracking_conf=config.TRACKING_CONFIDENCE
        )

    def test_blank_frame_processing(self):
        # Verify execution on synthetic 640x480 black frame
        blank_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        processed = self.detector.find_hands(blank_frame, draw=False)
        self.assertEqual(processed.shape, (480, 640, 3))

        landmarks = self.detector.get_landmarks(processed)
        self.assertEqual(landmarks, [])

        fingers = self.detector.fingers_up()
        self.assertEqual(fingers, [False, False, False, False, False])

    def test_euclidean_distance_calculation(self):
        # Populate synthetic landmark coordinates
        # Landmark 4 (Thumb tip) at (4, 100, 100)
        # Landmark 8 (Index tip) at (8, 130, 140)
        # Distance = sqrt((130 - 100)^2 + (140 - 100)^2) = sqrt(30^2 + 40^2) = 50.0
        synthetic_landmarks = [(i, 0, 0) for i in range(21)]
        synthetic_landmarks[4] = (4, 100, 100)
        synthetic_landmarks[8] = (8, 130, 140)
        self.detector.landmarks = synthetic_landmarks

        dist, _, info = self.detector.find_distance(4, 8, frame=None, draw=False)
        self.assertAlmostEqual(dist, 50.0, places=2)
        self.assertEqual(info, [100, 100, 130, 140, 115, 120])

    def test_fingers_up_evaluation(self):
        # Create synthetic 21 landmarks
        # Tip y < PIP y => Finger UP
        # Tip y >= PIP y => Finger DOWN
        synthetic_landmarks = [(i, 0, 300) for i in range(21)]

        # Index extended: Tip (8) y=150, PIP (6) y=250
        synthetic_landmarks[8] = (8, 200, 150)
        synthetic_landmarks[6] = (6, 200, 250)

        # Middle folded: Tip (12) y=280, PIP (10) y=220
        synthetic_landmarks[12] = (12, 230, 280)
        synthetic_landmarks[10] = (10, 230, 220)

        # Ring folded: Tip (16) y=280, PIP (14) y=220
        synthetic_landmarks[16] = (16, 260, 280)
        synthetic_landmarks[14] = (14, 260, 220)

        # Pinky folded: Tip (20) y=280, PIP (18) y=220
        synthetic_landmarks[20] = (20, 290, 280)
        synthetic_landmarks[18] = (18, 290, 220)

        # Thumb: folded horizontally (Tip 4 x < IP 3 x)
        synthetic_landmarks[4] = (4, 120, 260)
        synthetic_landmarks[3] = (3, 150, 260)

        self.detector.landmarks = synthetic_landmarks
        fingers = self.detector.fingers_up()
        self.assertEqual(fingers, [False, True, False, False, False])


class TestEndToEndPipelineIntegration(unittest.TestCase):
    """Tests the interaction between detector, classifier, and mouse controller."""

    @patch('src.mouse_controller.pyautogui')
    def test_pipeline_point_and_move_action(self, mock_pyautogui):
        mock_pyautogui.size.return_value = (1920, 1080)
        detector = HandDetector()
        controller = GestureController(buffer_size=4)
        mouse = MouseController(smoothening=1)

        # Synthetic pointing landmarks
        synthetic_landmarks = [(i, 0, 300) for i in range(21)]
        synthetic_landmarks[8] = (8, 320, 240)  # Index tip at frame center
        synthetic_landmarks[6] = (6, 320, 350)  # Index PIP lower
        synthetic_landmarks[4] = (4, 100, 300)
        synthetic_landmarks[3] = (3, 120, 300)
        detector.landmarks = synthetic_landmarks

        fingers = detector.fingers_up()
        dist, _, _ = detector.find_distance(4, 8, frame=None, draw=False)

        # Two consecutive frames of POINT
        controller.detect_gesture(fingers, pinch_distance=dist)
        gesture = controller.detect_gesture(fingers, pinch_distance=dist)
        self.assertEqual(gesture, "POINT")

        # Dispatch POINT action
        if gesture == "POINT":
            index_x, index_y = synthetic_landmarks[8][1], synthetic_landmarks[8][2]
            mouse.move(index_x, index_y, config.FRAME_REDUCTION, config.CAM_WIDTH, config.CAM_HEIGHT)

        mock_pyautogui.moveTo.assert_called_once()
        target_x, target_y = mock_pyautogui.moveTo.call_args[0]
        self.assertAlmostEqual(target_x, 960.0, places=1)
        self.assertAlmostEqual(target_y, 540.0, places=1)


if __name__ == "__main__":
    unittest.main()
