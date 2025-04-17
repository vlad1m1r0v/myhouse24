FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y gcc libpq-dev netcat-openbsd \
    libpango-1.0-0 libpangoft2-1.0-0 gir1.2-harfbuzz-0.0 && \
    apt clean && \
    rm -rf /var/cache/apt/*

COPY ../../pyproject.toml ../../poetry.lock /app/
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --only main --no-root


COPY . /app/

WORKDIR /app

CMD ["celery", "-A", "config", "worker", "--loglevel=info"]