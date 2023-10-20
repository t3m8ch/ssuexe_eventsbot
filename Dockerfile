FROM python:3.11 as building

WORKDIR /app

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100

RUN python3.11 -m venv venv
ENV PATH="/app/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.11-slim AS running

WORKDIR /app

COPY --from=building /app/venv venv

ENV VIRTUAL_ENV=/app/venv
ENV PATH=/app/venv/bin:$PATH

COPY . .

CMD alembic upgrade head && python3 main.py
