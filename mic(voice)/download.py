# download_vosk_medium.py
import urllib.request
import os
import zipfile

print("Downloading Vosk Medium English model (~300MB)...")
print("This may take some time.")

url = "https://alphacephei.com/kaldi/models/vosk-model-en-us-0.22.zip"
filepath = "models/vosk/vosk-model-en-us-0.22.zip"

os.makedirs("models/vosk", exist_ok=True)

urllib.request.urlretrieve(url, filepath)

print("Download finished. Extracting...")

with zipfile.ZipFile(filepath, 'r') as zip_ref:
    zip_ref.extractall("models/vosk")

print("✅ Vosk Medium model downloaded and extracted successfully!")
print("Folder: models/vosk/vosk-model-en-us-0.22")