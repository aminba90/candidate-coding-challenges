# syntax=docker/dockerfile:1

FROM python:3.8




WORKDIR /assignment

COPY ./requirements.txt /assignment/requirements.txt


RUN pip3 install -r requirements.txt


COPY . .