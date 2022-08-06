FROM node:12.10.0-alpine

WORKDIR /frontend

ENV PATH /web-front/node_modules/.bin:$PATH

COPY ./DesafioJunior-frontend/package.json .
COPY ./DesafioJunior-frontend/package-lock.json .
RUN npm install

COPY ./DesafioJunior-frontend ./
