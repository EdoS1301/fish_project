FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p staticfiles

EXPOSE 8000

CMD ["gunicorn", "fish.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
