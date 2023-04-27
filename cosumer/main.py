from config import CliArgsParser, ClientGenerator
from twitter_model_consumer import FakeDataConsumer
from utility.logger import logging
from utility.generic_configs import Topics


def main() -> None:
    """Starting point of the producer system"""
    cli_args_parser = CliArgsParser()
    cli_args = cli_args_parser.parser.parse_args()

    clients = ClientGenerator(cli_args)

    consumer = FakeDataConsumer(consumer=clients.consumer, topics=Topics())
    consumer.consume()


if __name__ == "__main__":
    main()
