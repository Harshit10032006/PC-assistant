import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "mic(voice)"))

from command import VoiceControl
import time

if __name__ == "__main__":
    vc = VoiceControl()
    vc.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        vc.stop()
