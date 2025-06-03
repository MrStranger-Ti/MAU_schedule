FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

RUN pip install --upgrade pip poetry
RUN poetry config virtualenvs.create false --local
COPY ./pyproject.toml ./pyproject.toml
RUN poetry install --without test,dev

COPY app/ .
