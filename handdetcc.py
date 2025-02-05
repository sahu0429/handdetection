import cv2
import numpy as np
import mediapipe as mp
from collections import deque

# Initialize Mediapipe Hand Model
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Colors for drawing
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
colorIndex = 0

# Initialize deque for different colors
bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]

blue_index = 0
green_index = 0
red_index = 0
yellow_index = 0

# Canvas setup
paintWindow = np.ones((471, 636, 3), dtype=np.uint8) * 255
cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

# Webcam capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Flip for mirror effect
    h, w, c = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hands
    result = hands.process(rgb_frame)
    index_finger_tip = None

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Extract the fingertip (Index Finger - Landmark 8)
            index_finger_tip = hand_landmarks.landmark[8]
            ix, iy = int(index_finger_tip.x * w), int(index_finger_tip.y * h)

            # Check if the user is selecting a color or clear
            if iy <= 65:
                if 40 <= ix <= 140:  # Clear Button
                    bpoints = [deque(maxlen=1024)]
                    gpoints = [deque(maxlen=1024)]
                    rpoints = [deque(maxlen=1024)]
                    ypoints = [deque(maxlen=1024)]
                    blue_index = green_index = red_index = yellow_index = 0
                    paintWindow[67:, :, :] = 255  # Reset canvas
                elif 160 <= ix <= 255:
                    colorIndex = 0  # Blue
                elif 275 <= ix <= 370:
                    colorIndex = 1  # Green
                elif 390 <= ix <= 485:
                    colorIndex = 2  # Red
                elif 505 <= ix <= 600:
                    colorIndex = 3  # Yellow
            else:
                # Drawing based on fingertip position
                if colorIndex == 0:
                    bpoints[blue_index].appendleft((ix, iy))
                elif colorIndex == 1:
                    gpoints[green_index].appendleft((ix, iy))
                elif colorIndex == 2:
                    rpoints[red_index].appendleft((ix, iy))
                elif colorIndex == 3:
                    ypoints[yellow_index].appendleft((ix, iy))

    # Draw the color buttons on the frame
    cv2.rectangle(frame, (40, 1), (140, 65), (122, 122, 122), -1)
    cv2.rectangle(frame, (160, 1), (255, 65), colors[0], -1)
    cv2.rectangle(frame, (275, 1), (370, 65), colors[1], -1)
    cv2.rectangle(frame, (390, 1), (485, 65), colors[2], -1)
    cv2.rectangle(frame, (505, 1), (600, 65), colors[3], -1)

    cv2.putText(frame, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 2, cv2.LINE_AA)

    # Draw on the Paint Window
    points = [bpoints, gpoints, rpoints, ypoints]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k - 1] is None or points[i][j][k] is None:
                    continue
                cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)

    # Show frames
    cv2.imshow("Hand Gesture Drawing", frame)
    cv2.imshow("Paint", paintWindow)

    # Exit condition
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
