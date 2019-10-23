FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /antiplag
WORKDIR /antiplag
COPY ./antiplag /antiplag

RUN adduser -D user
USER user