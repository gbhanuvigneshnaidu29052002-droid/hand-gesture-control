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

### 📐 System Architecture & Mathematical Formulation

The touchless control framework processes video streams through a four-stage pipeline:

#### 1. Landmark Topology Extraction
- Uses **MediaPipe Hands** to detect 21 3D hand keypoints $(x_i, y_i, z_i)$ per frame.
- Normalized keypoints $(x_i, y_i) \in [0, 1]^2$ are mapped to OS display bounds $(W_{\text{screen}}, H_{\text{screen}})$.

#### 2. Kinematic State Classification
Finger elevation states are evaluated by comparing distal fingertip positions ($y_{\text{tip}}$) against proximal interphalangeal joints ($y_{\text{PIP}}$):

```math
\text{FingerState}_i = \begin{cases} 1 & \text{if } y_{\text{tip}, i} < y_{\text{PIP}, i} \quad (\text{Finger Extended}) \\ 0 & \text{if } y_{\text{tip}, i} \ge y_{\text{PIP}, i} \quad (\text{Finger Folded}) \end{cases}
```

- **Pinch Thresholding:** Spatial Euclidean distance between Thumb Tip ($P_4$) and Index Tip ($P_8$):
```math
D_{\text{pinch}} = \sqrt{(x_8 - x_4)^2 + (y_8 - y_4)^2} < 30\text{ px}
```

#### 3. Cursor Kinematics & Exponential Smoothing
Sub-pixel cursor movement uses Exponential Moving Average (EMA) filtering to eliminate high-frequency hand tremor:

```math
P_{\text{curr}} = P_{\text{prev}} + \frac{P_{\text{target}} - P_{\text{prev}}}{\alpha} \quad (\text{where } \alpha = 5)
```

#### 4. Temporal Hysteresis Majority Voting
To eliminate transient landmark flicker:
- Maintains a sliding history buffer of size $N = 4$ frames: $\mathcal{H} = [g_{t-3}, g_{t-2}, g_{t-1}, g_t]$.
- Active gesture $G_{\text{output}} = \text{mode}(\mathcal{H})$ dispatches actions only when supported by consecutive frames.

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