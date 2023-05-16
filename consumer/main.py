from time import sleep

from sqlalchemy.orm import Session

from model.twitter_database_model import Base
from dabase_writer import DatabaseWriter
from config import CliArgsParser, ClientGenerator
from twitter_model_consumer import FakeDataConsumer
from utility.generic_configs import Topics


def main() -> None:
    """Starting point of the producer system"""
    # TODO: Find a good way to wait for the producer to be ready
    sleep(5)

    cli_args_parser = CliArgsParser()
    cli_args = cli_args_parser.parser.parse_args()

    clients = ClientGenerator(cli_args)

    # Create tables
    Base.metadata.create_all(clients.db_engine)

    with Session(clients.db_engine) as session:
        db_writer = DatabaseWriter(db_session=session)
        consumer = FakeDataConsumer(
            consumer=clients.consumer, topics=Topics(), db_writer=db_writer
        )
        consumer.consume()


if __name__ == "__main__":
    main()
