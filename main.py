from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from TTS.api import TTS
from io import BytesIO
import soundfile as sf
import re

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load TTS model
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)


class TTSRequest(BaseModel):
    text: str


def clean_special_chars(text):
    # Replace newlines with pauses (e.g., period + space)
    text = text.replace('\n', '. ')
    return re.sub(r'[^a-zA-Z0-9\s\.\,\?\!\:\;]', '', text)


@app.post("/tts/speak", response_class=StreamingResponse)
async def speak(request: TTSRequest):
    text = clean_special_chars(request.text.strip())
    text = text + "."
    print(text)

    if not text:
        raise HTTPException(status_code=400, detail="No text provided")

    try:
        # Synthesize speech
        waveform = tts.tts(text=text, max_decoder_steps=20000)

        # Save to in-memory WAV
        buffer = BytesIO()
        sf.write(buffer, waveform,
                 samplerate=tts.synthesizer.output_sample_rate, format="WAV")
        buffer.seek(0)

        return StreamingResponse(buffer, media_type="audio/wav")

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"TTS generation failed: {str(e)}")
