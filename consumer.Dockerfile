FROM python:3.11-slim-bullseye

WORKDIR /consumer

COPY requirements.txt requirements.txt

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

RUN pip3 install -r requirements.txt

COPY . .

ENV PYTHONPATH "${PYTHONPATH}:/consumer"

CMD ["python3", "consumer/main.py", \
    "-b", "localhost:9092", \
    "-s", "http://localhost:8081", \
    "-g", "Consumer1", \
    "--db-ip", "127.0.0.1", \
    "--db-user", "postgres", \
    "--db-password", "postgres", \
    "--db-name", "twitter"]
