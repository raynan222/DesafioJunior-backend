FROM postgres:14.0-alpine

ARG POSTGRES_PASSWORD=postgres
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD

ARG NEW_USER=postgres
ENV POSTGRES_NEW_USER=$NEW_USER

ARG NEW_DATABASE=web_app
ENV POSTGRES_NEW_DATABASE=$NEW_DATABASE

ADD desafioJunior-backend/build/config/postgres.conf /etc/postgresql/postgresql.conf

