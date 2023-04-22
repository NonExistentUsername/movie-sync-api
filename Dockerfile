FROM python:3.10.7-slim

RUN apt-get -y update && apt-get -y upgrade

ENV PYTHONFAULTHANDLER=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random 

RUN pip3 install --no-cache "poetry==1.4.0" && poetry --version

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-dev --no-root