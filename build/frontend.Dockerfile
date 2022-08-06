FROM node:12.10.0-alpine

WORKDIR /frontend

ENV PATH /web-front/node_modules/.bin:$PATH

COPY ./desafioJunior-frontend/package.json .
COPY ./desafioJunior-frontend/package-lock.json .
RUN npm install

COPY ./desafioJunior-frontend ./
