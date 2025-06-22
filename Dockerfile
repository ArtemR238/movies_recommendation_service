FROM python:3.11-slim

ENV OPENBLAS_NUM_THREADS=1

RUN apt-get update && \
    apt-get install -y \
      build-essential \
      libpq-dev \
      git \
      postgresql-client \
      curl \
      unzip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x ./entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["sh", "/app/entrypoint.sh"]



