import urllib.request
import os

os.makedirs("models", exist_ok=True)
url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
filepath = "models/hand_landmarker.task"

if not os.path.exists(filepath):
    print("Downloading Hand Landmarker model...")
    urllib.request.urlretrieve(url, filepath)
    print("Download complete!")
else:
    print("Model already downloaded.")