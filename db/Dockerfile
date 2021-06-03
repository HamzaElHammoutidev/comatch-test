FROM postgres:latest
ENV POSTGRES_PASSWORD=root
ENV POSTGRES_USER=root
ENV POSTGRES_DB=weather
COPY create_table.sql /docker-entrypoint-initdb.d/create_table.sql