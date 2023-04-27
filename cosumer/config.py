import argparse

from confluent_kafka import Consumer


class ClientGenerator:
    """Class for generating required objects based on given CLI configs."""

    def __init__(self, args: argparse.Namespace) -> None:
        self.consumer = self._get_consumer_client(
            bootstrap_servers=args.kafka_bootstrap_servers,
            consumer_group=args.consumer_group,
            reset_offset=args.reset_offset,
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
