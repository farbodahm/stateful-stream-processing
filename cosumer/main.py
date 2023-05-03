from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from model.twitter_database_model import Base
from dabase_writer import DatabaseWriter
from config import CliArgsParser, ClientGenerator
from twitter_model_consumer import FakeDataConsumer
from utility.logger import logging
from utility.generic_configs import Topics


DB_ENGINE = create_engine(
    "postgresql+psycopg2://postgres:postgres@localhost:5432/twitter", echo=True
)


def main() -> None:
    """Starting point of the producer system"""
    cli_args_parser = CliArgsParser()
    cli_args = cli_args_parser.parser.parse_args()

    clients = ClientGenerator(cli_args)

    # Create tables
    Base.metadata.create_all(DB_ENGINE)

    with Session(DB_ENGINE) as session:
        db_writer = DatabaseWriter(db_session=session)
        consumer = FakeDataConsumer(
            consumer=clients.consumer, topics=Topics(), db_writer=db_writer
        )
        consumer.consume()


if __name__ == "__main__":
    main()
