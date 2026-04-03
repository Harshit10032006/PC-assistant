import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import pyautogui
import time

pyautogui.FAILSAFE = False

base_options = python.BaseOptions(model_asset_path="models/hand_landmarker.task")

options = vision.HandLandmarkerOptions(base_options=base_options,
    num_hands=1,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.7,min_tracking_confidence=0.7)

detector = vision.HandLandmarker.create_from_options(options)
screen_w, screen_h = pyautogui.size()
prev_x, prev_y = 0, 0
smoothing = 0.9 
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

last_click_time = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    detection_result = detector.detect(mp_image)

    if detection_result.hand_landmarks:
        for hand_landmarks in detection_result.hand_landmarks:
           
            for i, landmark in enumerate(hand_landmarks):
                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])
                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

            
            index_tip = hand_landmarks[8]   
            thumb_tip = hand_landmarks[4]   

            
            index_x = int(index_tip.x * frame.shape[1])
            index_y = int(index_tip.y * frame.shape[0])

            cursor_x = int(index_tip.x * screen_w)
            cursor_y = int(index_tip.y * screen_h)

            cursor_x = int(prev_x * smoothing + cursor_x * (1 - smoothing))
            cursor_y = int(prev_y * smoothing + cursor_y * (1 - smoothing))
            prev_x, prev_y = cursor_x, cursor_y

            pyautogui.moveTo(cursor_x, cursor_y, duration=0.01)

            thumb_x = thumb_tip.x
            thumb_y = thumb_tip.y
            distance = ((index_tip.x - thumb_x)**2 + (index_tip.y - thumb_y)**2) ** 0.5

            current_time = time.time()
            if distance < 0.05 and (current_time - last_click_time > 0.5):
                pyautogui.click()
                last_click_time = current_time
                cv2.putText(frame, "CLICK!", (index_x + 20, index_y), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            cv2.putText(frame, "Index Finger Controls Mouse", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("Virtual Mouse - Hand Signs PC Assistant", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Virtual Mouse stopped.")