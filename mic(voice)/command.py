import json
import queue
import sounddevice as sd
import vosk
import threading
import subprocess
import pyautogui
import ctypes
import os

class VoiceControl:
    def __init__(self):
        self.model = None
        self.recognizer = None
        self.is_listening = False
        self.audio_queue = queue.Queue()

        self.commands = {
            "volume up":        lambda: pyautogui.press("volumeup"),
            "increase volume":  lambda: pyautogui.press("volumeup"),
            "volume down":      lambda: pyautogui.press("volumedown"),
            "decrease volume":  lambda: pyautogui.press("volumedown"),
            "mute":             lambda: pyautogui.press("volumemute"),
            "lock screen":      lambda: ctypes.windll.user32.LockWorkStation(),
            "shutdown":         lambda: subprocess.run("shutdown /s /t 10", shell=True),
            "restart":          lambda: subprocess.run("shutdown /r /t 10", shell=True),
            "sleep":            lambda: subprocess.run("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", shell=True),
            "open chrome":      lambda: subprocess.run('start chrome', shell=True),
            "chrome":           lambda: subprocess.run('start chrome', shell=True),
            "open brave":       lambda: subprocess.run('start brave', shell=True),
            "brave":            lambda: subprocess.run('start brave', shell=True),
            "open cursor":      lambda: subprocess.run('start cursor', shell=True),
            "cursor":           lambda: subprocess.run('start cursor', shell=True),
            "show desktop":     lambda: pyautogui.hotkey("win", "d"),
            "play pause":       lambda: pyautogui.press("space"),
        }

    def load_model(self):
        model_path = "models/vosk/vosk-model-en-us-0.22"

        if not os.path.exists(model_path):
            return False

        self.model = vosk.Model(model_path)
        self.recognizer = vosk.KaldiRecognizer(self.model, 16000)
        return True

    def start(self):
        if not self.load_model():
            return

        self.is_listening = True

        def listener():
            def callback(indata, frames, time_info, status):
                self.audio_queue.put(bytes(indata))

            with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                                   channels=1, callback=callback):
                while self.is_listening:
                    try:
                        data = self.audio_queue.get(timeout=0.5)
                        if self.recognizer.AcceptWaveform(data):
                            result = json.loads(self.recognizer.Result())
                            text = result.get("text", "").strip().lower()

                            if text:
                                self.execute_command(text)
                    except:
                        pass

        threading.Thread(target=listener, daemon=True).start()

    def execute_command(self, text):
        for cmd, action in self.commands.items():
            if cmd in text:
                try:
                    action()
                    return
                except Exception:
                    pass

    def stop(self):
        self.is_listening = False
