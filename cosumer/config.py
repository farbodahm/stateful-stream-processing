import argparse

from confluent_kafka import Consumer
from sqlalchemy import create_engine
from sqlalchemy import Engine


class ClientGenerator:
    """Class for generating required objects based on given CLI configs."""

    def __init__(self, args: argparse.Namespace) -> None:
        self.consumer = self._get_consumer_client(
            bootstrap_servers=args.kafka_bootstrap_servers,
            consumer_group=args.consumer_group,
            reset_offset=args.reset_offset,
        )

        self.db_engine = self._get_db_engine(
            ip=args.database_ip,
            port=args.database_port,
            username=args.database_username,
            password=args.database_password,
            db_name=args.database_name,
        )

    def _get_consumer_client(
        self, bootstrap_servers: str, consumer_group: str, reset_offset: bool
    ) -> Consumer:
        """Create and return Kafka Consumer client."""

        consumer_conf = {
            "bootstrap.servers": bootstrap_servers,
            "group.id": consumer_group,
        }

        if reset_offset:
            consumer_conf = {
                **consumer_conf,
                "auto.offset.reset": "earliest",
                "enable.auto.commit": False,
            }

        consumer = Consumer(consumer_conf)

        return consumer

    def _get_db_engine(
        self, ip: str, port: str, username: str, password: str, db_name: str
    ) -> Engine:
        """Create and return SQLAlchemy Engine object."""
        db_url = f"postgresql+psycopg2://{username}:{password}@{ip}:{port}/{db_name}"
        engine = create_engine(db_url, echo=True)

        return engine


class CliArgsParser:
    """Class for generating required ArgParse arguments"""

    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            description=(
                "Service for consuming fake Twitter data in Kafka topics and writing "
                "them to databse."
            )
        )

        self._add_arguments()

    def _add_arguments(self) -> None:
        """Add arguments that parser needs to parse."""
        self.parser.add_argument(
            "-b",
            dest="kafka_bootstrap_servers",
            required=True,
            help="Bootstrap broker(s) (host[:port])",
        )
        self.parser.add_argument(
            "-s",
            dest="schema_registry",
            required=True,
            help="Schema Registry (http(s)://host[:port]",
        )
        self.parser.add_argument(
            "-g",
            dest="consumer_group",
            default="Twitter-Model-Consumer",
            help="Consumer group name",
        )
        self.parser.add_argument(
            "-c",
            dest="reset_offset",
            default=True,
            action="store_true",
            help="Reset offset to earliest",
        )
        self.parser.add_argument(
            "--db-ip",
            dest="database_ip",
            default="localhost",
            help="Databse IP",
        )
        self.parser.add_argument(
            "--db-port",
            dest="database_port",
            default="5432",
            help="Databse Port",
        )
        self.parser.add_argument(
            "--db-user",
            dest="database_username",
            default="postgres",
            help="Databse Username",
        )
        self.parser.add_argument(
            "--db-password",
            dest="database_password",
            default="postgres",
            help="Databse Password",
        )
        self.parser.add_argument(
            "--db-name",
            dest="database_name",
            default="twitter",
            help="Databse Name",
        )
