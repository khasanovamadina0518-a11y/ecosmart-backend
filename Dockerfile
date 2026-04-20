# ── Base Image ────────────────────────────────────
FROM python:3.11-slim

# ── Working Directory ─────────────────────────────
WORKDIR /app

# ── Environment Variables ─────────────────────────
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

# ── Install System Dependencies ───────────────────
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# ── Copy Requirements ─────────────────────────────
COPY requirements.txt .

# ── Install Python Dependencies ───────────────────
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ── Copy Application Code ─────────────────────────
COPY . .

# ── Expose Port ───────────────────────────────────
EXPOSE $PORT

# ── Run Application ───────────────────────────────
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
