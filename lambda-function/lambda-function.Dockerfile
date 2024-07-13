# syntax=docker/dockerfile:1
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PIP_ROOT_USER_ACTION=ignore

WORKDIR /lambda-function

RUN apt-get update \
    && apt-get install -y build-essential libpq-dev postgresql-client --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /lambda-function

RUN pip install -U pip --no-cache-dir && pip install --requirement requirements.txt --no-cache-dir

COPY . /lambda-function

RUN chmod +x /lambda-function/lambda-function.entrypoint.sh

ENTRYPOINT ["/lambda-function/lambda-function.entrypoint.sh"]
