FROM python:3.11-slim-bullseye
ARG KAFKA_BROKER
ARG SCHEMA_REGISTRY_URL
ARG CONSUMER_GROUP
ARG DB_HOST
ARG DB_PORT
ARG DB_USERNAME
ARG DB_PASSWORD
ARG DB_NAME

WORKDIR /consumer

COPY requirements.txt requirements.txt

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

RUN pip3 install -r requirements.txt

COPY . .

ENV PYTHONPATH "${PYTHONPATH}:/consumer"
# Convert build time arguments to runtime env variables
ENV KAFKA_BROKER ${KAFKA_BROKER}
ENV SCHEMA_REGISTRY_URL ${SCHEMA_REGISTRY_URL}
ENV CONSUMER_GROUP ${CONSUMER_GROUP}
ENV DB_HOST ${DB_HOST}
ENV DB_PORT ${DB_PORT} 
ENV DB_USERNAME ${DB_USERNAME}
ENV DB_PASSWORD ${DB_PASSWORD}
ENV DB_NAME ${DB_NAME}

CMD exec python3 consumer/main.py \
    -b ${KAFKA_BROKER} \
    -s ${SCHEMA_REGISTRY_URL} \
    -g ${CONSUMER_GROUP} \
    --db-ip ${DB_HOST} \
    --db-port ${DB_PORT} \
    --db-user ${DB_USERNAME} \
    --db-password ${DB_PASSWORD} \
    --db-name ${DB_NAME}
