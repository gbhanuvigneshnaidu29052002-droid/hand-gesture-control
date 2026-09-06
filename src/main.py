"""
Module entry point for Hand Gesture Control.
Author: Bhanu Vignesh Naidu Ganeshna
"""

import os
import sys

# Ensure repository root is on Python search path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import run_controller


def main():
    """Run real-time gesture controller."""
    run_controller()


if __name__ == "__main__":
    main()