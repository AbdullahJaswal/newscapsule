# syntax=docker/dockerfile:1
FROM node:18-buster-slim

WORKDIR /frontend

RUN apt-get update \
    && apt-get install -y build-essential ca-certificates --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

COPY package.json /frontend/

RUN npm install --loglevel verbose

COPY . /frontend/

RUN chmod +x dev.entrypoint.sh
