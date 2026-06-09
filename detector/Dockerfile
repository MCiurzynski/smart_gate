FROM nvidia/cuda:13.1.2-base-ubuntu24.04

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libxcb1 \
    && rm -rf /var/lib/apt/lists/*

ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1

COPY --from=ghcr.io/astral-sh/uv:0.11.14 /uv /uvx /bin/

WORKDIR /app

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

COPY uv.lock pyproject.toml ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Lepiej nic nie zmieniać przed tym komentarzem bo obraz bedzie się długo tworzył
ENV YOLO_CONFIG_DIR=/
ENV YOLO_PATH=models/best.pt
ENV LICENSE_PLATE_OCR=cct-xs-v2-global-model

RUN mkdir Ultralytics

COPY models/ models/

COPY main.py .
COPY src/ ./src

# USER appuser

CMD ["uv", "run", "--no-dev", "main.py"]