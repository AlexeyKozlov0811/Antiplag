FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /antiplag
WORKDIR /antiplag
COPY . /antiplag

RUN python antiplag/manage.py migrate
