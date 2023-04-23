import random
from time import sleep

from config import CliArgsParser, ClientGenerator, TOPICS_TO_PRODUCING_PROBABILITY
from twitter_model_producer import FakeDataProducer
from exceptions import NotFoundError
from logger import logging

TOPICS = [
    topic for topic in TOPICS_TO_PRODUCING_PROBABILITY.keys()
]
PROBABILITIES = [
    probability for probability in TOPICS_TO_PRODUCING_PROBABILITY.values()
]


def get_next_topic() -> str:
    """Returns next topic name to produce data based on given """
    topic = random.choices(TOPICS, weights=PROBABILITIES)[0]
    return topic


def generate_fake_data(producer: FakeDataProducer) -> None:
    """Main unlimited loop for generating fake data"""
    while True:
        topic = get_next_topic()
        logging.info(f"Producing data to topic: {topic}")
        try:
            producer.produce_to_topic(topic=topic)
        except NotFoundError as e:
            # Pass the not found exceptions as in the next call, resource may be created
            logging.error(e)

        sleep(2)

    # TODO: Gracefully kill the application
    # producer.producer.flush()


def main() -> None:
    """Starting point of the producer system"""
    cli_args_parser = CliArgsParser()
    cli_args = cli_args_parser.parser.parse_args()

    clients = ClientGenerator(cli_args)
    producer = FakeDataProducer(
        producer=clients.producer, schema_registry_client=clients.schema_registry_client
    )

    generate_fake_data(producer=producer)


if __name__ == "__main__":
    main()
