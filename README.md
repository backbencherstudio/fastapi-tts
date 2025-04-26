# Description
TTS app

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