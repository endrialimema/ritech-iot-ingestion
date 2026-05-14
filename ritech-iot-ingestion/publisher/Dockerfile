# ----------------------------
# Stage 1: build dependencies
# ----------------------------
FROM python:3.11-slim AS builder

WORKDIR /app

# system deps (optional but good practice)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt


# ----------------------------
# Stage 2: runtime image
# ----------------------------
FROM python:3.11-slim AS runtime

WORKDIR /app

# copy installed packages from builder
COPY --from=builder /install /usr/local

# copy application code
COPY publisher.py .

# run as non-root (good practice)
RUN useradd -m appuser
USER appuser

CMD ["python", "-u","-m", "publisher.py"]