FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    g++ \
    python3-dev \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --prefix=/install -r requirements.txt

COPY app ./app

WORKDIR /app/app/core/cpp_normalizer
RUN PYTHONPATH=/install/lib/python3.11/site-packages python setup.py build_ext --inplace


FROM python:3.11-slim AS runtime

WORKDIR /app

COPY --from=builder /install /usr/local
COPY --from=builder /app/app ./app

ENV PYTHONPATH=/app

CMD ["python", "-m", "app.mqtt_subscriber"]
