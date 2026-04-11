import cv2 
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import pyautogui
import joblib
import time 
import numpy as np
import subprocess
import ctypes


model=joblib.load("models/gesture_model.pkl")

print('Done')


base_options = python.BaseOptions(model_asset_path="models/hand_landmarker.task")
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=2,
    min_hand_detection_confidence=0.75,
    min_hand_presence_confidence=0.7,
    min_tracking_confidence=0.7
)
detector = vision.HandLandmarker.create_from_options(options)

gesture_rules = {
    "thumbs_up":    lambda: pyautogui.press("volumeup"),                    
    "thumb_down":   lambda: pyautogui.press("volumedown"),                  
    "victory":      lambda: subprocess.run(["start", "chrome"], shell=True), 
    "open_palm":    lambda: pyautogui.hotkey("win", "d"),                   
    "ok_sign":      lambda: pyautogui.press("space"),                       
    "cool":         lambda: subprocess.run(["start", "brave"], shell=True),
    "middle":       lambda: ctypes.windll.user32.LockWorkStation(),}

for gesture in gesture_rules:
    print(f"   {gesture:12} → Assigned")


cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    detection_result = detector.detect(mp_image)

    current_gesture = "No Hand"
    confidence = 0.0

    if detection_result.hand_landmarks:
        hand_landmarks = detection_result.hand_landmarks[0]

        
        features = []
        for landmark in hand_landmarks:
            features.extend([landmark.x, landmark.y, landmark.z])
        features = np.array(features).reshape(1, -1)

        prediction = model.predict(features)[0]
        confidence = model.predict_proba(features).max()

        current_gesture = prediction

        for landmark in hand_landmarks:
            x = int(landmark.x * frame.shape[1])
            y = int(landmark.y * frame.shape[0])
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

        if confidence > 0.40 and current_gesture in gesture_rules:
            try:
                gesture_rules[current_gesture]()
                
                cv2.putText(frame, f" {current_gesture.upper()}", (30, 160),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 255), 4)
                time.sleep(0.7)
            except Exception as e:
                print(f"Error: {e}")

    cv2.putText(frame, f"Gesture: {current_gesture}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 255, 0), 3)
    cv2.putText(frame, f"Confidence: {confidence:.2f}", (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow("Hand Gesture PC Assistant", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()