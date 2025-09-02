# app/Dockerfile

FROM python:3.13-slim

WORKDIR /var/www

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip

COPY requirements.txt .

RUN pip3 install -r requirements.txt

WORKDIR /var/www/app

COPY ./app .

HEALTHCHECK CMD curl --fail http://localhost:$PORT/_stcore/health

