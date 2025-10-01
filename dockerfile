FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    postgresql-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --shell /bin/bash app
USER app
WORKDIR /home/app

COPY --chown=app:app requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем ВЕСЬ проект включая static/
COPY --chown=app:app . .

RUN mkdir -p staticfiles

EXPOSE 8000

CMD ["gunicorn", "fish.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]