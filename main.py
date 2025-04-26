from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
# from TTS.api import TTS
# import soundfile as sf
import io
import re
import fitz
import requests
from gtts import gTTS
import os
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
# tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)


class TTSRequest(BaseModel):
    text: str


class PDFRequest(BaseModel):
    url: str


def clean_special_chars(text):
    # Replace newlines with period + space to simulate pause
    text = text.replace('\n', '. ')
    # Replace non-breaking spaces with regular spaces
    text = text.replace('\u00A0', ' ')
    # Remove unwanted characters, but keep useful punctuation
    text = re.sub(r'[^a-zA-Z0-9\s\.\,\?\!\:\;]', '', text)
    return text.strip()


def download_file(url: str) -> bytes:
    """Download file and return as bytes"""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(
            f'Failed to download file. Status code: {response.status_code}')


@app.post("/parse-pdf")
async def parse_pdf(request: PDFRequest):
    try:
        file_bytes = download_file(request.url)

        pdf = fitz.open(stream=file_bytes, filetype="pdf")
        text = ""

        for page in pdf:
            text += page.get_text()

        pdf.close()

        return JSONResponse(content={"content": text})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tts/speak", response_class=StreamingResponse)
async def speak(request: TTSRequest):
    text = clean_special_chars(request.text.strip())
    text = text + "."
    print(text)

    if not text:
        raise HTTPException(status_code=400, detail="No text provided")

    try:
        # Synthesize speech
        # waveform = tts.tts(text=text, max_decoder_steps=20000)

        # Save to in-memory WAV
        # buffer = BytesIO()
        # sf.write(buffer, waveform,
        #          samplerate=tts.synthesizer.output_sample_rate, format="WAV")
        # buffer.seek(0)

        tts = gTTS(text, lang='en')
        buffer = io.BytesIO()
        tts.write_to_fp(buffer)
        buffer.seek(0)  # Rewind to the beginning of the buffer

        return StreamingResponse(buffer, media_type="audio/mp3")

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"TTS generation failed: {str(e)}")
