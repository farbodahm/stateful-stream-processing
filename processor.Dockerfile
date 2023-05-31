FROM python:3.11-slim-bullseye

ARG DB_HOST
ARG DB_PORT
ARG DB_USERNAME
ARG DB_PASSWORD
ARG DB_NAME
ARG WS_HOST
ARG WS_PORT
ARG WS_WRITE_POOL_SIZE

WORKDIR /processor

COPY requirements.txt requirements.txt

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

RUN pip3 install -r requirements.txt

COPY . .

ENV PYTHONPATH "${PYTHONPATH}:/processor"
# Convert build time arguments to runtime env variables
ENV DB_HOST ${DB_HOST}
ENV DB_PORT ${DB_PORT} 
ENV DB_USERNAME ${DB_USERNAME}
ENV DB_PASSWORD ${DB_PASSWORD}
ENV DB_NAME ${DB_NAME}
ENV WS_HOST ${WS_HOST}
ENV WS_PORT ${WS_PORT}
ENV WS_WRITE_POOL_SIZE ${WS_WRITE_POOL_SIZE}

EXPOSE ${WS_PORT}

CMD exec python3 processor/main.py \
    --db-ip ${DB_HOST} \
    --db-port ${DB_PORT} \
    --db-user ${DB_USERNAME} \
    --db-password ${DB_PASSWORD} \
    --db-name ${DB_NAME} \
    --ws-host ${WS_HOST} \
    --ws-port ${WS_PORT} \
    --ws-write-pool-size ${WS_WRITE_POOL_SIZE}
