FROM python:3.12-alpine

RUN pip install --no-cache-dir uv && \
    python -m uv venv /venv

ENV PATH="/venv/bin:$PATH"

WORKDIR /app

COPY pyproject.toml uv.lock* ./
RUN uv pip install --no-cache -e .
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000