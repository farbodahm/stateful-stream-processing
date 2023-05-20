import argparse

from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient


class ClientGenerator:
    """Class for generating required objects based on given CLI configs."""

    def __init__(self, args: argparse.Namespace) -> None:
        self.schema_registry_client = self._get_schema_registry_client(
            url=args.schema_registry_url
        )

        self.producer = self._get_producer_client(
            bootstrap_servers=args.kafka_bootstrap_servers,
        )

    def _get_schema_registry_client(self, url: str) -> SchemaRegistryClient:
        """Create and return schema registry client."""
        schema_registry_conf = {
            "url": url,
        }
        client = SchemaRegistryClient(conf=schema_registry_conf)

        return client

    def _get_producer_client(self, bootstrap_servers: str) -> Producer:
        """Create and return Kafka producer client."""
        producer_conf = {
            "bootstrap.servers": bootstrap_servers,
            "receive.message.max.bytes": 1500000000,
        }
        producer = Producer(producer_conf)

        return producer


class CliArgsParser:
    """Class for generating required ArgParse arguments"""

    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            description="Service for generating fake Twitter data in Kafka topics."
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
            dest="schema_registry_url",
            required=True,
            help="Schema Registry (http(s)://host[:port]",
        )
