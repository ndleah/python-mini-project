FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    python3-tk \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

CMD ["python3", "Caterpillar.py"]
