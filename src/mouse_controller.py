import pyautogui
import numpy as np

# Disable failsafe and default pause for maximum 30+ FPS non-blocking execution
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

class MouseController:
    """
    Handles high-performance mouse movement, click actions, scrolling, and dragging.
    """

    def __init__(self, smoothening=4):
        self.prev_x, self.prev_y = 0, 0
        self.smoothening = max(1, smoothening)
        self.screen_w, self.screen_h = pyautogui.size()
        self.is_dragging = False

    def move(self, x, y, frame_reduction, cam_w, cam_h):
        """
        Move cursor based on hand position with exponential smoothing
        """
        x3 = np.interp(x, (frame_reduction, cam_w - frame_reduction), (0, self.screen_w))
        y3 = np.interp(y, (frame_reduction, cam_h - frame_reduction), (0, self.screen_h))

        curr_x = self.prev_x + (x3 - self.prev_x) / self.smoothening
        curr_y = self.prev_y + (y3 - self.prev_y) / self.smoothening

        pyautogui.moveTo(curr_x, curr_y, _pause=False)
        self.prev_x, self.prev_y = curr_x, curr_y

    def click(self):
        """Perform single left click"""
        pyautogui.click(_pause=False)

    def double_click(self):
        """Perform double left click"""
        pyautogui.doubleClick(_pause=False)

    def right_click(self):
        """Perform right click"""
        pyautogui.rightClick(_pause=False)

    def scroll_up(self, amount=250):
        """Scroll window up"""
        pyautogui.scroll(amount, _pause=False)

    def scroll_down(self, amount=250):
        """Scroll window down"""
        pyautogui.scroll(-amount, _pause=False)

    def start_drag(self):
        """Press and hold mouse button for dragging"""
        if not self.is_dragging:
            pyautogui.mouseDown(_pause=False)
            self.is_dragging = True

    def stop_drag(self):
        """Release mouse button after dragging"""
        if self.is_dragging:
            pyautogui.mouseUp(_pause=False)
            self.is_dragging = False