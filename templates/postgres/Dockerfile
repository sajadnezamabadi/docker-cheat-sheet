FROM postgres:15-alpine

# Copy initialization scripts
COPY init.sql /docker-entrypoint-initdb.d/

# Set environment variables
ENV POSTGRES_DB=mydb
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres

# Create data directory
VOLUME ["/var/lib/postgresql/data"]

EXPOSE 5432

CMD ["postgres"]

