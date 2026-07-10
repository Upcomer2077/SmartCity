FROM python:3.14 AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV UV_COMPILE_BYTECODE=1

WORKDIR /simulator

COPY uv.lock pyproject.toml .python-version ./
COPY transmitter/pyproject.toml transmitter/
COPY emitter/pyproject.toml emitter/
COPY collector/pyproject.toml collector/
COPY common/pyproject.toml common/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-editable

COPY common/ common/

RUN --mount=type=cache,target=/root/.cache/uv \ 
    uv sync --frozen --all-packages --no-editable


FROM python:3.14-slim AS runner
ENV PYTHONUNBUFFERED=1

WORKDIR /simulator

COPY --from=builder /simulator/.venv/ .venv/

COPY transmitter/ transmitter/
COPY emitter/ emitter/
COPY collector/ collector/
COPY config.py main.py ./

CMD ["python", "main.py"]
