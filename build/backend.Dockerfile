FROM python:3.9.13-slim

WORKDIR /backend

RUN apt-get update -y
RUN apt-get install -y locales locales-all
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

RUN pip install poetry

COPY ./DesafioJunior-backend/build/poetry.lock .
COPY ./DesafioJunior-backend/build/pyproject.toml .

RUN poetry config virtualenvs.create false
RUN poetry install

COPY ./DesafioJunior-backend ./
