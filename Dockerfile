# pull official base image
FROM python:3.9.6-alpine

RUN mkdir /auth_service

# set work directory
WORKDIR /auth_service

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install dependencies
RUN apk update && apk add --virtual build-deps gcc
RUN /usr/local/bin/python -m pip install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN /usr/local/bin/python -m pip install -r /requirements.txt

# copy project
COPY . .