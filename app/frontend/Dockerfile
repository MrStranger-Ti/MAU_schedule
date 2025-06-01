FROM node:19.9.0

WORKDIR /usr/app/

COPY ./package.json ./package.json
COPY ./package-lock.json ./package-lock.json

RUN npm install

COPY ./public ./public
COPY ./src ./src
