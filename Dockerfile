FROM python:3.11-slim AS builder

WORKDIR /app

# system deps for C++ build
RUN apt-get update && apt-get install -y \
    build-essential \
    g++ \
    python3-dev \
 && rm -rf /var/lib/apt/lists/*

# install python deps
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# copy full app
COPY app ./app

# build C++ extension
WORKDIR /app/app/core/cpp_normalizer
RUN python setup.py build_ext --inplace


# -------------------------
# runtime image
# -------------------------
FROM python:3.11-slim AS runtime

WORKDIR /app

COPY --from=builder /usr/local /usr/local
COPY --from=builder /app/app ./app

ENV PYTHONPATH=/app

CMD ["python", "-m", "app.mqtt_subscriber"]
