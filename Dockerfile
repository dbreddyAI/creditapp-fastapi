FROM tiangolo/uvicorn-gunicorn-fastapi:python3.6

MAINTAINER ramottamado

RUN mkdir -p /creditscore/app
WORKDIR /creditscore

COPY . /creditscore
RUN pip install -r requirements.txt
WORKDIR /creditscore/app
