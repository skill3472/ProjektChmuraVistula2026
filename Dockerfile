FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y curl \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

COPY . .

EXPOSE 80

RUN useradd -m fastapi \
    && chown -R fastapi:fastapi /app

USER fastapi

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]