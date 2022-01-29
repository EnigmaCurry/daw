FROM python:3

## Install poetry:
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

WORKDIR /app

## Install project dependencies:
COPY ./pyproject.toml ./poetry.lock* /app/
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        pulseaudio-utils libasound2-plugins ffmpeg libasound2-dev && \
    poetry install --no-root --no-dev

ENV PYTHONPATH=/app

## Install the application code:
## (commented out in DEV mode, because will just mount this directory from host)
## COPY . /app

## Setup audio to run through the *host* pulseaudio server:
COPY asound.conf /etc/asound.conf
COPY pulse-client.conf /etc/pulse/client.conf
