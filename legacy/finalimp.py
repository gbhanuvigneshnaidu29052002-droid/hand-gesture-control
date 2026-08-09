import cv2
import numpy as np
import mediapipe as mp
import time
from pynput.mouse import Controller, Button

####################################
# Configuration
wCam, hCam = 640, 480
frameR_outer = 100
frameR_inner = 150
smoothening = 7
####################################

mouse = Controller()

class HandDetector:
    def __init__(self, mode=False, maxHands=1, detectionCon=0.7, trackCon=0.7):
        self.mpHands = mp.solutions.hands
        self.hands   = self.mpHands.Hands(
            static_image_mode=mode,
            max_num_hands=maxHands,
            min_detection_confidence=detectionCon,
            min_tracking_confidence=trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
        self.lmList = []

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks and draw:
            for handLms in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(
                    img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0):
        self.lmList = []
        if not self.results.multi_hand_landmarks:
            return []
        hand = self.results.multi_hand_landmarks[handNo]
        h, w, _ = img.shape
        for id, lm in enumerate(hand.landmark):
            self.lmList.append((id, int(lm.x*w), int(lm.y*h)))
        return self.lmList

    def fingersUp(self):
        if not self.lmList:
            return [False]*5
        fingers = []
        # Thumb
        fingers.append(self.lmList[4][1] > self.lmList[3][1])
        # Index, middle, ring, pinky
        for tip, pip in zip([8,12,16,20], [6,10,14,18]):
            fingers.append(self.lmList[tip][2] < self.lmList[pip][2])
        return fingers


# Initialize variables
pTime = 0
plocx, plocy = 0, 0
clocx, clocy = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam); cap.set(4, hCam)
detector = HandDetector()

print("Press 'q' to quit")

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    fingers = detector.fingersUp()
    gesture = "No Hand"

    # Draw purple outer boundary
    cv2.rectangle(img,
        (frameR_outer, frameR_outer),
        (wCam-frameR_outer, hCam-frameR_outer),
        (255, 0, 255), 2)

    # Dynamic green inner boundary
    if lmList:
        xs = [pt[1] for pt in lmList]
        ys = [pt[2] for pt in lmList]
        pad = 20
        xmin, xmax = max(min(xs)-pad,0), min(max(xs)+pad,wCam)
        ymin, ymax = max(min(ys)-pad,0), min(max(ys)+pad,hCam)
    else:
        xmin, ymin = frameR_inner, frameR_inner
        xmax, ymax = wCam-frameR_inner, hCam-frameR_inner

    cv2.rectangle(img,
        (xmin, ymin),
        (xmax, ymax),
        (0, 255, 0), 2)

    # Red circles at thumb, index, middle tips
    for tip in [4, 8, 12]:
        if lmList:
            cv2.circle(img,
                (lmList[tip][1], lmList[tip][2]),
                8, (0, 0, 255), cv2.FILLED)

    # 1. Pointing: only index up
    if fingers[1] and not fingers[2] and not fingers[3]:
        x, y = lmList[8][1], lmList[8][2]
        x3 = np.interp(x,
            (frameR_outer, wCam-frameR_outer),
            (0, 1920))
        y3 = np.interp(y,
            (frameR_outer, hCam-frameR_outer),
            (0, 1080))
        clocx = plocx + (x3-plocx)/smoothening
        clocy = plocy + (y3-plocy)/smoothening
        mouse.position = (clocx, clocy)
        plocx, plocy = clocx, clocy
        gesture = "Pointing"

    # 2. Single Click: index + middle up
    elif fingers[1] and fingers[2] and not fingers[3]:
        mouse.click(Button.left, 1)
        gesture = "Single Click"
        time.sleep(0.3)

    # 3. Double Click: index + middle + ring up
    elif fingers[1] and fingers[2] and fingers[3]:
        mouse.click(Button.left, 2)
        gesture = "Double Click"
        time.sleep(0.3)

    # Display FPS and status
    cTime = time.time()
    fps = 1/(cTime-pTime); pTime = cTime
    cv2.putText(img, f'FPS:{int(fps)}', (10,30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0),2)
    cv2.putText(img, gesture, (10,60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0),2)
    cv2.putText(img, "Press 'q' to quit", (10,hCam-20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255),2)

    cv2.imshow("gestures_with_exit", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()