import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import pandas as pd
import os
import time
base_options = python.BaseOptions(model_asset_path="models/hand_landmarker.task")
options = vision.HandLandmarkerOptions(
    base_options=base_options,num_hands=1,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.7,
    min_tracking_confidence=0.7)
detector = vision.HandLandmarker.create_from_options(options)
gestures = {
    '0': 'open_palm',
    '1': 'cool',
    '2': 'thumbs_up',
    '3': 'victory',
    '4': 'middle','5': 'ok_sign','6': 'thumb_down'}

os.makedirs("data", exist_ok=True)
csv_path = "data/hand_gestures.csv"

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
else:
    df = pd.DataFrame()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

collected_count = {name: 0 for name in gestures.values()}

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    detection_result = detector.detect(mp_image)

    gesture_text = "No Hand"

    if detection_result.hand_landmarks:
        hand_landmarks = detection_result.hand_landmarks[0]

        for landmark in hand_landmarks:
            x = int(landmark.x * frame.shape[1])
            y = int(landmark.y * frame.shape[0])
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

        gesture_text = "Show gesture & press number"

    cv2.putText(frame, "Data Collection Mode", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    cv2.putText(frame, gesture_text, (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    y_offset = 110
    for key, name in gestures.items():
        count = collected_count.get(name, 0)
        cv2.putText(frame, f"{key}: {name} ({count})", (10, y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        y_offset += 25

    cv2.imshow("Gesture Data Collection - Press number to save", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

    if chr(key) in gestures and detection_result.hand_landmarks:
        gesture_name = gestures[chr(key)]
        hand_landmarks = detection_result.hand_landmarks[0]


        row = []
        for landmark in hand_landmarks:
            row.extend([landmark.x, landmark.y, landmark.z])

        
        row.append(gesture_name)

        
        new_row = pd.DataFrame([row], columns=[f'lm_{i}' for i in range(63)] + ['label'])
        df = pd.concat([df, new_row], ignore_index=True)

        collected_count[gesture_name] += 1
        
        time.sleep(0.3)

if not df.empty:
    df.to_csv(csv_path, index=False)

cap.release()
cv2.destroyAllWindows()