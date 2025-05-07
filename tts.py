from google.cloud import texttospeech
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-account-key.json"

# Initialize client
client = texttospeech.TextToSpeechClient()

# Define the input text
synthesis_input = texttospeech.SynthesisInput(
    text="Hello! This is the Chirp3 HD voice Algenib speaking.")

# Configure the voice request
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US",
    name="en-US-chirp3-HD-Algenib",
    ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
)

# Configure audio settings (MP3 in this case)
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# Perform the TTS request
response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

# Save the output
with open("output.mp3", "wb") as out:
    out.write(response.audio_content)
    print(response.audio_content)
    print("Audio content written to output.mp3")
