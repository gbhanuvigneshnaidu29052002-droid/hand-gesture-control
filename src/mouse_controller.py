import pyautogui
import numpy as np

# Disable failsafe (prevents crash when cursor hits screen corner)
pyautogui.FAILSAFE = False

class MouseController:
    """
    Handles mouse movement and click actions
    """

    def __init__(self, smoothening):
        # Previous cursor position
        self.prev_x, self.prev_y = 0, 0

        # Smoothening factor
        self.smoothening = smoothening

        # Get screen resolution
        self.screen_w, self.screen_h = pyautogui.size()

    def move(self, x, y, frame_reduction, cam_w, cam_h):
        """
        Move cursor based on hand position
        """

        # Convert camera coordinates to screen coordinates
        x3 = np.interp(x, (frame_reduction, cam_w - frame_reduction), (0, self.screen_w))
        y3 = np.interp(y, (frame_reduction, cam_h - frame_reduction), (0, self.screen_h))

        # Apply smoothing
        curr_x = self.prev_x + (x3 - self.prev_x) / self.smoothening
        curr_y = self.prev_y + (y3 - self.prev_y) / self.smoothening

        # Move mouse
        pyautogui.moveTo(curr_x, curr_y)

        # Update previous position
        self.prev_x, self.prev_y = curr_x, curr_y

    def click(self):
        """Perform single click"""
        pyautogui.click()

    def double_click(self):
        """Perform double click"""
        pyautogui.click()
        pyautogui.click()