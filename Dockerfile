FROM python:3.11

WORKDIR /app

COPY requirements.txt .

# Install system dependencies
RUN apt-get update && apt-get install -y \
    espeak \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Pre-install CPU-only PyTorch and torchaudio (skip CUDA)
RUN pip install --no-cache-dir torch==2.0.1+cpu torchaudio==2.0.2+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html

# Install Coqui TTS and FastAPI-related dependencies
RUN pip install --no-cache-dir git+https://github.com/coqui-ai/TTS.git fastapi uvicorn[standard]

# RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

