FROM python:3.11-slim-bullseye
ARG KAFKA_BROKER
ARG SCHEMA_REGISTRY_URL
ARG SAMPLE_TWITTER_DATA_PATH

WORKDIR /producer

COPY requirements.txt requirements.txt

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

RUN pip3 install -r requirements.txt

COPY . .

ENV PYTHONPATH "${PYTHONPATH}:/producer"
# Convert build time arguments to runtime env variables
ENV KAFKA_BROKER ${KAFKA_BROKER}
ENV SCHEMA_REGISTRY_URL ${SCHEMA_REGISTRY_URL}
ENV SAMPLE_TWITTER_DATA_PATH ${SAMPLE_TWITTER_DATA_PATH}


CMD exec python3 producer/main.py \
    -b ${KAFKA_BROKER} \
    -s ${SCHEMA_REGISTRY_URL} \
    --sample-twitter-data-path ${SAMPLE_TWITTER_DATA_PATH}
