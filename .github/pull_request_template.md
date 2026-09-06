## Description
A clear and concise summary of the changes introduced in this pull request.

## Related Issue(s)
Fixes #(issue number) or Addresses #(issue number)

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding new gesture or functionality)
- [ ] Performance optimization (improving FPS, latency, or memory footprint)
- [ ] Documentation update (improving guides, README, or docstrings)
- [ ] Automated testing (adding unit tests or simulation fixtures)

## Verification & Testing Checklist
- [ ] Dependencies install cleanly via `pip install -r requirements.txt`
- [ ] Automated unit test suite passes:
  ```bash
  python3 -m unittest discover -s tests -v
  ```
- [ ] Code follows project architecture (`src/hand_detector.py`, `src/gesture_controller.py`, `src/mouse_controller.py`)
- [ ] Main controller operates in non-blocking mode maintaining $\ge 30\text{ FPS}$
- [ ] No regression introduced to existing gestures (`POINT`, `DRAG`, `CLICK`, `DOUBLE_CLICK`, `RIGHT_CLICK`, `PALM_SCROLL`)
- [ ] Configuration variables documented and cleanly organized in `config.py`
