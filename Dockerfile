FROM python:3.15-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:0.5.7 /uv /bin/uv

ENV \
    # do not buffer python output at all
    PYTHONUNBUFFERED=1 \
    # do not write `__pycache__` bytecode
    PYTHONDONTWRITEBYTECODE=1


WORKDIR /app

COPY . .

RUN uv sync \
        --frozen \
        --compile-bytecode \
        --no-editable \
        --no-dev

FROM python:3.15-slim AS runtime

ENV PATH="/app/.venv/bin:$PATH"

COPY --from=builder /app/.venv /app/.venv

WORKDIR /app

ENTRYPOINT [ "python", "-m", "cost_gateway.main", "--config", "/app/config.yaml"]
