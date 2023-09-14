FROM mcr.microsoft.com/devcontainers/python:0-3.11

COPY pyproject.toml ./

ENV PYTHONUNBUFFERED 1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=0 \
    POETRY_VIRTUALENVS_CREATE=0 \
    PIP_DEFAULT_TIMEOUT=100\
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN pip install poetry &&\
    poetry install --no-root &&\
    rm -rf $POETRY_CACHE_DIR
