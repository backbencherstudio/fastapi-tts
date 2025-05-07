# Description

TTS app

# Setup

Windows:
https://github.com/tesseract-ocr/tesseract/releases
Download the official installer from GitHub (e.g., tesseract-ocr-w64-setup.exe)

Install it, and add the installation path to your system's PATH environment variable

Linux (Debian/Ubuntu):

```
sudo apt update
sudo apt install tesseract-ocr
```

# Run

```
# dev
fastapi dev main.py
or
uvicorn main:app --reload
# production
uvicorn main:app --host 0.0.0.0 --port 8000
```

# Usage

```
curl -X POST http://localhost:8000/tts/speak -H "Content-Type: application/json" -d '{"text": "Hello Sojeb"}' --output output.wav
```
