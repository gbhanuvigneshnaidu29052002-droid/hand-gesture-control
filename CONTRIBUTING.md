# Contributing to Hand Gesture Control

Thank you for your interest in contributing to **Real-Time Touchless Human-Computer Interaction via Hand Gesture Control**! We welcome contributions from computer vision developers, HCI researchers, and open-source contributors.

Please read through this guide before submitting issues or pull requests.

---

## Code of Conduct

All contributors and participants are expected to adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). Please report any unacceptable behavior to the project maintainer.

---

## Areas of Contribution

We encourage contributions across several computer vision and HCI domains:

- **Gesture Vocabulary Expansion**: Add support for novel gesture patterns (e.g., volume control gestures, swipe navigation, virtual zoom, three-finger window cycling).
- **Multi-Hand Coordination**: Extend tracking pipeline to support bimanual interactions (e.g., two-handed resizing or 3D canvas manipulation).
- **Tracking Resilience & Lighting Adaptation**: Implement automatic contrast balancing (CLAHE) or skin tone adaptation for extreme illumination environments.
- **Cross-Platform OS Automation**: Expand input backend support across Linux (X11 / Wayland via `ydotool`), macOS (Quartz), and Windows.
- **Edge Deployment & Acceleration**: Implement TensorRT or ONNX Runtime inference pipelines for ultra-low latency on embedded platforms (NVIDIA Jetson, Raspberry Pi).

---

## Reporting Issues & Bugs

Before opening a new issue, please check existing [GitHub Issues](https://github.com/gbhanuvigneshnaidu29052002-droid/hand-gesture-control/issues) to avoid duplicates.

When reporting a bug:
1. Use our [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.md).
2. Specify your environment details:
   - OS: Linux (Ubuntu) / Windows / macOS (specify Wayland or X11 if on Linux)
   - Python Version: Python 3.10+
   - OpenCV Version: OpenCV 4.x
   - MediaPipe Version: MediaPipe 0.10.x
   - Camera Type: Integrated webcam, external USB camera, or virtual camera
3. Include clear steps to reproduce the issue and observed vs expected behavior.
4. Attach relevant terminal logs, stack traces, or frame screenshots.

---

## Development Workflow

### 1. Fork & Clone Repository
```bash
git clone https://github.com/<your-username>/hand-gesture-control.git
cd hand-gesture-control
```

### 2. Set Up Virtual Environment & Dependencies
```bash
python3 -m venv .venv

# On Linux / macOS:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 4. Run Automated Tests
Before submitting changes, ensure all tests pass cleanly:
```bash
python3 -m unittest discover -s tests -v
```

### 5. Commit & Push Changes
Follow conventional commit messages:
- `feat: Add three-finger swipe gesture for workspace switching`
- `fix: Resolve boundary clamping issue in multi-monitor setups`
- `docs: Improve camera calibration instructions in README`
- `test: Add unit test coverage for pinch distance calculations`

```bash
git add .
git commit -m "feat: Describe your feature cleanly"
git push origin feature/your-feature-name
```

### 6. Open a Pull Request
Submit your PR against the `main` branch using our [Pull Request Template](.github/pull_request_template.md).

---

## Code Style & Guidelines

- **PEP 8 Compliance**: Follow PEP 8 style conventions for clean, readable code.
- **Modularity**: Keep detection (`src/hand_detector.py`), gesture classification (`src/gesture_controller.py`), and OS interaction (`src/mouse_controller.py`) decoupled.
- **Configuration Centralization**: Place all tunable thresholds (smoothing factors, cooldowns, bounding reductions) inside `config.py`.
- **Non-Blocking Performance**: Do not introduce blocking loops or synchronous sleep calls inside the core frame processing loop to sustain 30+ FPS.

---

## Recognition

Contributors who have meaningful pull requests merged will be acknowledged in the project documentation. Thank you for helping advance touchless human-computer interaction!
