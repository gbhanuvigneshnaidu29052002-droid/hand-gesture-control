# Real-Time Touchless Human-Computer Interaction via Hand Gesture Control

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https.python.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green.svg)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Landmark%20Tracking-orange.svg)](https://google.github.io/mediapipe/)
[![License](https://img.shields.io/badge/License-MIT-brightgreen.svg)](LICENSE)

**Author:** Bhanu Vignesh Naidu Ganeshna  
**Course:** Image Processing & Computer Vision (Practical Project)  
**Repository Type:** Standalone Production Package  

---

## 📌 Executive Summary & Project Overview

### A. Short Summary
* **Goal:** Design and deploy a high-performance, real-time touchless desktop controller using webcam feedback, MediaPipe 3D hand landmark tracking, kinematic gesture state classification, and sub-pixel smooth cursor kinematics.
* **Key Innovations:**
  - **High FPS Non-Blocking Pipeline:** Achieved **30+ FPS** on standard CPU hardware by disabling default PyAutoGUI blocking delays (`pyautogui.PAUSE = 0`), eliminating blocking `time.sleep` calls, and employing lightweight MediaPipe model complexity (`model_complexity=0`).
  - **Temporal Hysteresis Majority Voting:** Integrated a 4-frame sliding buffer to eliminate single-frame landmark jitter, flickering, and accidental gesture switching.
  - **Intuitive Palm Motion Scroll:** Implemented vertical palm movement tracking (`PALM_SCROLL`) for natural, velocity-proportional page scrolling.
  - **Pinch-Based Drag & Drop:** Separated pointing navigation from dragging via strict thumb-index Euclidean distance thresholding ($< 30\text{ px}$).

---

### B. Supported Gesture Controls

| Gesture State | Finger Configuration / Trigger Condition | Mapped Action |
| :--- | :--- | :--- |
| **`POINT`** | Only Index Finger UP | Smooth Cursor Navigation (Independent of Thumb) |
| **`DRAG`** | Thumb-Index Pinch ($< 30\text{ px}$) | Press, Hold & Drag Element / Window |
| **`CLICK`** | Index + Middle Fingers UP | Non-Blocking Single Left Click |
| **`DOUBLE_CLICK`** | Index + Middle + Ring Fingers UP | Double Left Click |
| **`RIGHT_CLICK`** | Index + Pinky Fingers UP | Right Click / Context Menu |
| **`PALM_SCROLL`** | Open Palm (All 4 Main Fingers UP) | Move Palm **UP** to Scroll Up / **DOWN** to Scroll Down |

---

### C. System Architecture & Setup

1. **Landmark Extraction:** MediaPipe Hands (21 3D joint coordinates).
2. **Kinematic Classification:** Rule-based vertical joint elevation comparison:
   $$\text{FingerState}_i = \begin{cases} 1 & \text{if } y_{\text{tip}, i} < y_{\text{PIP}, i} \\ 0 & \text{otherwise} \end{cases}$$
3. **Exponential Moving Average (EMA) Smoothing:**
   $$\vec{P}_{\text{curr}} = \vec{P}_{\text{prev}} + \frac{\vec{P}_{\text{target}} - \vec{P}_{\text{prev}}}{\alpha}$$
   where $\alpha = 5$ for ultra-smooth motion.
4. **Temporal Stability Filtering:** Majority voting over 4 consecutive frames.

---

## 🛠️ Installation & Usage

### 1. Prerequisites
- Python 3.10+
- Webcam

### 2. Quick Setup
```bash
# Clone the repository
git clone https://github.com/gbhanuvigneshnaidu29052002-droid/hand-gesture-control.git
cd hand-gesture-control

# Activate virtual environment
..\.venv\Scripts\Activate.ps1

# Run live gesture controller
python main.py
```

---

### 📝 Declaration of Original Work

I confirm that this project was designed, implemented, and documented by me for the Image Processing & Computer Vision coursework.

**Author:** Bhanu Vignesh Naidu Ganeshna  
**License:** MIT License