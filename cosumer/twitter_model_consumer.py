from typing import Dict, List
from dataclasses import fields

from confluent_kafka import Consumer, Message as KafkaMessage
from confluent_kafka.schema_registry.protobuf import ProtobufDeserializer
from confluent_kafka.serialization import SerializationContext, MessageField
from google.protobuf.message import Message

from model import twitter_pb2
from dabase_writer import DatabaseWriter
from utility.generic_configs import Topics
from utility.logger import logging
from utility.exceptions import ProtobufDeserializerNotFound


class FakeDataConsumer:
    """Main class for consuming Twitter data from Kafka."""

    def __init__(
        self, consumer: Consumer, topics: Topics, db_writer: DatabaseWriter
    ) -> None:
        self.consumer = consumer
        self.db_writer = db_writer

        # Subscribe to given topics
        topics: List[str] = [topic.default for topic in fields(Topics)]
        logging.info(f"Subscribing to topics: {topics}")
        self.consumer.subscribe(topics)

        # Deserializers
        self.deserializers = self._get_deserializers()

    def consume(self) -> None:
        """Consume data from Kafka."""

        logging.info("Starting to consume data from Kafka.")

        while True:
            message: KafkaMessage = self.consumer.poll(timeout=1.0)
            if message is None:
                continue

            topic = message.topic()
            if message.error() is not None:
                logging.error(
                    f"Error while consuming data from {topic}: {message.error()}"
                )
                continue

            logging.info(f"Consumed message from topic {topic}")

            protobuf_message = self._deserialize_message(message)

            try:
                self._process_message(protobuf_message, topic)
            except Exception as e:
                logging.error(
                    f"Error while processing message {protobuf_message} from {topic}: {e}"
                )

        # TODO: Gracefully close consumer
        # consumer.close()

    def _process_message(self, protobuf_message: Message, topic: str) -> None:
        """Process recieved Protobuf message."""
        # TODO: Remove after tests finished
        logging.info(f"Processing from {topic} message {protobuf_message}")

        if topic == Topics.UsersTopic:
            self.db_writer.write_to_database(topic=topic, message=protobuf_message)

    def _get_deserializers(self) -> Dict[str, ProtobufDeserializer]:
        """Map each topic to its Protobuf Deserializer."""

        deserializers: Dict[str, ProtobufDeserializer] = {
            Topics.TweetsTopic: ProtobufDeserializer(
                twitter_pb2.Tweet, {"use.deprecated.format": False}
            ),
            Topics.UsersTopic: ProtobufDeserializer(
                twitter_pb2.User, {"use.deprecated.format": False}
            ),
            Topics.CommentsTopic: ProtobufDeserializer(
                twitter_pb2.Comment, {"use.deprecated.format": False}
            ),
            Topics.TweetLikesTopic: ProtobufDeserializer(
                twitter_pb2.TweetLike, {"use.deprecated.format": False}
            ),
            Topics.UserFollowsTopic: ProtobufDeserializer(
                twitter_pb2.UserFollow, {"use.deprecated.format": False}
            ),
        }

        return deserializers

    def _deserialize_message(self, message: KafkaMessage) -> Message:
        """Deserialize message from Kafka to Protobuf message."""

        protobuf_deserializer = self.deserializers.get(message.topic(), None)
        if protobuf_deserializer is None:
            raise ProtobufDeserializerNotFound(
                f"Deserializer for {message.topic()} not found."
            )

        protobuf_message = protobuf_deserializer(
            message.value(), SerializationContext(message.topic(), MessageField.VALUE)
        )

        return protobuf_message
