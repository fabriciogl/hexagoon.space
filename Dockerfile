# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.10

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True
ENV ENV_FOR_DYNACONF production
ENV GOOGLE_APPLICATION_CREDENTIALS auth_gcp.json
ENV TNS_ADMIN oracle_client/network/admin
ENV LD_LIBRARY_PATH oracle_client
ENV DPI_DEBUG_LEVEL 64
# OPTIONS e PORT serão passados pelo docker-compose

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./


# instal curl
# RUN apt update && apt upgrade
RUN apt install -y curl

RUN apt-get update && apt-get upgrade
RUN apt-get install libaio1 libaio-dev

# install poetry
RUN pip install poetry


# Install production dependencies.
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.

# line of command for local development
# EXPOSE 8000
# CMD exec gunicorn --bind 0.0.0.0:8000 --workers 1 --worker-class uvicorn.workers.UvicornWorker --threads 8 --timeout 0 main:app

# line of command for GCP
CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker --threads 8 --timeout 0 $OPTIONS main:app

# call from terminal
# gcloud run deploy hexagoon --add-cloudsql-instances "hexsaturn:us-east1:db-hexagoon"