import random
from time import sleep
from typing import List


from config import CliArgsParser, ClientGenerator
from twitter_model_producer import FakeDataProducer
from utility.exceptions import NotFoundError
from utility.logger import logger
from utility.generic_configs import TOPICS_TO_PRODUCING_PROBABILITY
from utility.generic_configs import Topics
from model_faker import FakeDataModel

TOPICS = [topic for topic in TOPICS_TO_PRODUCING_PROBABILITY.keys()]
PROBABILITIES = [
    probability for probability in TOPICS_TO_PRODUCING_PROBABILITY.values()
]


def get_texts(path: str) -> List[str]:
    """Returns list of texts from the given file"""
    with open(path, "r") as file:
        lines = file.readlines()
        return lines


def get_next_topic() -> str:
    """Returns next topic name to produce data based on given"""
    topic = random.choices(TOPICS, weights=PROBABILITIES)[0]
    return topic


def generate_fake_data(producer: FakeDataProducer) -> None:
    """Main unlimited loop for generating fake data"""
    intialize_topics(producer=producer)

    while True:
        topic = get_next_topic()
        logger.info(f"Producing data to topic: {topic}")
        try:
            producer.produce_to_topic(topic=topic)
        except NotFoundError as e:
            # Pass the not found exceptions as in the next call, resource may be created
            logger.error(e)

        sleep(2)

    # TODO: Gracefully kill the application
    # producer.producer.flush()


def intialize_topics(producer: FakeDataProducer) -> None:
    """Initialize topics for first time based on the correct logical order of topics"""
    # TODO: Use Confluent AdminClient for creating topics
    logger.info("Creating topics...")
    topics_ordered = [
        Topics.UsersTopic,
        Topics.TweetsTopic,
        Topics.CommentsTopic,
        Topics.TweetLikesTopic,
        Topics.UsersTopic,
        Topics.UserFollowsTopic,
    ]

    for topic in topics_ordered:
        logger.info(f"Creating topic: {topic}")
        try:
            producer.produce_to_topic(topic=topic)
        except Exception as e:
            logger.error(
                f"Error in initializing topic: {topic}.",
                exc_info=True,
            )
            raise e


def main() -> None:
    """Starting point of the producer system"""
    cli_args_parser = CliArgsParser()
    cli_args = cli_args_parser.parser.parse_args()

    clients = ClientGenerator(cli_args)

    if cli_args.sample_twitter_data_path is not None:
        texts = get_texts(path=cli_args.sample_twitter_data_path)
        fake_data_generator = FakeDataModel(texts=texts)
    else:
        fake_data_generator = FakeDataModel()

    producer = FakeDataProducer(
        producer=clients.producer,
        schema_registry_client=clients.schema_registry_client,
        fake_data_generator=fake_data_generator,
    )

    generate_fake_data(producer=producer)


if __name__ == "__main__":
    main()
