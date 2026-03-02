FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3-gi \
    gir1.2-gstreamer-1.0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    python3-gst-1.0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt --break-system-packages

COPY . .

CMD ["python3", "main.py"]
