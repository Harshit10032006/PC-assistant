# assistant.py

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "mic(voice)"))

from command import VoiceControl
import time

if __name__ == "__main__":
    print("=" * 60)
    print("   AI Voice Assistant")
    print("=" * 60)

    vc = VoiceControl()
    vc.start()

    print("\nPress Ctrl + C to stop.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nAssistant stopped.")
        vc.stop()