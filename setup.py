from setuptools import setup, find_packages

setup(
    name="hand_gesture_control",
    version="1.0.0",
    description="Real-Time Touchless Human-Computer Interaction via Hand Gesture Control",
    author="Bhanu Vignesh Naidu Ganeshna",
    packages=find_packages(),
    install_requires=[
        "opencv-python>=4.5.0",
        "mediapipe>=0.8.9",
        "pyautogui>=0.9.53",
        "numpy>=1.21.0"
    ],
    entry_points={
        'console_scripts': [
            'gesture-control=main:run_controller',
        ],
    },
    python_requires='>=3.8',
)
