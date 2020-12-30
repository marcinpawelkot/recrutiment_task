FROM python:3.8.1-slim-buster

WORKDIR /app

RUN pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# app image without secrets
COPY . /app

