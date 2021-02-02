FROM python:3.8.3-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/newspy

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev \
    && apk add jpeg-dev zlib-dev libjpeg \
    && apk add bash


RUN pip install --upgrade pip

COPY ./requirements.in /usr/src/requirements.in
RUN pip install -r /usr/src/requirements.in

COPY . /usr/src/newspy
