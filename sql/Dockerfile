FROM postgres:14-alpine

ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_USER=postgres
ENV POSTGRES_DB=hobbyhorsing

COPY hh_sql.sql /docker-entrypoint-initdb.d/