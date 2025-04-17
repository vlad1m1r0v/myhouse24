FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y gcc libpq-dev netcat-openbsd \
    libpango-1.0-0 libpangoft2-1.0-0 gir1.2-harfbuzz-0.0 && \
    apt clean && \
    rm -rf /var/cache/apt/*

COPY ../../pyproject.toml ../../poetry.lock ./
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --only main --no-root

COPY . .

COPY deploy/web/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]