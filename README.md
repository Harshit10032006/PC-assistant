# 🖥️ AI PC Assistant (Voice + Hand Gesture Control)

A Python-based AI assistant that allows you to control your computer using **voice commands** and **hand gestures**.
This project combines **Computer Vision**, **Speech Recognition**, and **Automation** to create a touchless interaction system.

---

## 🚀 Features

* 🎤 Voice-controlled PC operations (offline using Vosk)
* ✋ Hand gesture recognition using MediaPipe
* 🖱️ Mouse & system control via gestures
* ⌨️ Keyboard automation using PyAutoGUI
* ⚡ Fast and lightweight (no cloud dependency)
* 🧠 Custom command mapping (fully configurable)

---

## 🛠️ Tech Stack

* **Python**
* **OpenCV (cv2)**
* **MediaPipe**
* **Vosk**
* **PyAutoGUI**
* **NumPy**
* **Joblib**
* **SoundDevice**
* **Threading & Queue**



---

## 🎮 Controls

### ✋ Hand Gestures

| Gesture          | Action             |
| ---------------- | ------------------ |
| 👍 Thumbs Up     | Volume Up          |
| 👎 Thumbs Down   | Volume Down        |
| ✌️ Victory       | Open Chrome        |
| 🖐️ Open Palm    | Show Desktop       |
| 👌 OK Sign       | Press Space        |
| 😎 Cool Gesture  | Open Brave Browser |
| 🖕 Middle Finger | Lock System        |

---


##  Voice Commands 

| Command        | Action              |
| -------------- | ------------------- |
| "Open Chrome"  | Launch browser      |
| "Close Window" | Close active window |
| "Volume Up"    | Increase volume     |
| "Shutdown"     | Turn off system     |

---

## 🧠 How It Works

1. Camera captures hand gestures using MediaPipe
2. Gestures are classified and mapped to actions
3. Microphone captures voice input using Vosk
4. Recognized commands trigger system actions
5. Multithreading enables parallel gesture + voice control

---

## ⚠️ Limitations

* No GUI (CLI-based)
* Gesture detection depends on lighting conditions
* Voice accuracy depends on microphone quality
* Limited command set (expandable)

---

## 🔮 Future Improvements

* GUI interface
* More gesture training
* Advanced NLP for voice commands
* App-specific automation
* Cross-platform support


