FROM python:3.11-slim-bullseye

WORKDIR /producer

COPY requirements.txt requirements.txt

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

RUN pip3 install -r requirements.txt

COPY . .

ENV PYTHONPATH "${PYTHONPATH}:/producer"

CMD ["python3", "producer/main.py", "-b", "localhost:9092", "-s", "http://localhost:8081"]