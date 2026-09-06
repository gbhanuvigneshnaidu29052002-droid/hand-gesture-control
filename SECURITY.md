# Security Policy

## Supported Versions

We actively support and release security fixes for the current release of **Real-Time Touchless Human-Computer Interaction via Hand Gesture Control**.

| Version | Supported          |
| :--- | :---: |
| 1.0.x | :white_check_mark: |
| < 1.0.0 | :x: |

---

## Threat Model & Considerations

Because this software interacts directly with the local operating system cursor and camera feed, please consider the following security considerations:

1. **Webcam Privacy**: The pipeline processes camera frames entirely locally in system memory. No video streams, biometric signatures, or images are transmitted over the network or saved to external storage.
2. **OS Input Automation**: The controller uses `pyautogui` for desktop input synthesis. Exercise caution when running touchless control while viewing sensitive administrative interfaces, terminal sessions with elevated privileges, or authentication prompts.
3. **Dependency Security**: Third-party packages (`mediapipe`, `opencv-python`, `pyautogui`) should be sourced from trusted PyPI indices.

---

## Reporting a Vulnerability

If you discover a security vulnerability within this repository, please report it responsibly:

1. **Do not disclose publicly**: Please refrain from opening a public GitHub issue detailing an active security vulnerability.
2. **Contact Maintainer**: Reach out directly to the maintainer via GitHub profile contact at [gbhanuvigneshnaidu29052002-droid](https://github.com/gbhanuvigneshnaidu29052002-droid) or submit a private security advisory through the GitHub repository's **Security** tab.
3. **Report Contents**:
   - Description of the vulnerability
   - Affected system components (`HandDetector`, `MouseController`, dependencies)
   - Step-by-step reproduction instructions or Proof-of-Concept (PoC)
   - Potential impact on local host security

We will acknowledge receipt within 48 hours and work on a prompt remediation.
