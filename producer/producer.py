from typing import Dict, Callable


from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka import Producer
from google.protobuf.message import Message

from model_faker import FakeDataModel
from model import twitter_pb2
from config import Topics


class FakeDataProducer:
    """Main class for generating next model and producing it in Kafka."""

    def __init__(self, producer: Producer, schema_registry_client: SchemaRegistryClient) -> None:
        self.faker = FakeDataModel()
        self.producer = producer
        self.schema_registry_client = schema_registry_client

        # Serializers
        self.string_serializer = StringSerializer('utf8')
        self.protobuf_serializers = self._get_serializers(
            schema_registry_client=self.schema_registry_client
        )

        self.topics_to_model_generators = self.get_topics_to_model_genarators()

    def produce(self, topic: str, key: str, msg: Message) -> None:
        """Produce given model to Kafka"""
        protobuf_serializer = self.protobuf_serializers[topic]

        self.producer.produce(topic=topic, partition=0,
                              key=self.string_serializer(key),
                              value=protobuf_serializer(
                                  msg, SerializationContext(topic, MessageField.VALUE)),
                              on_delivery=FakeDataProducer._delivery_report,)

    def produce_to_topic(self, topic: str) -> None:
        """Produce a fake generated model to the given topic"""
        generated_model = self.topics_to_model_generators[topic]()
        self.produce(topic=topic, key=generated_model.id, msg=generated_model)

    def get_topics_to_model_genarators(self) -> Dict[str, Callable]:
        """Map each topic to its relatated model generator function."""
        result: Dict[str, Callable] = {
            Topics.TweetsTopic: self.faker.generate_tweet_model,
            Topics.UsersTopic: self.faker.generate_user_model,
            Topics.CommentsTopic: self.faker.generate_comment_model,
            Topics.TweetLikesTopic: self.faker.generate_tweetlike_model,
            Topics.UserFollowsTopic: self.faker.generate_userfollow_model,
        }

        return result

    def _get_serializers(self, schema_registry_client: SchemaRegistryClient) -> Dict[str, ProtobufSerializer]:
        """Map each topic to its Protobuf Serializer."""

        serializers: Dict[str, ProtobufSerializer] = {
            Topics.TweetsTopic: ProtobufSerializer(twitter_pb2.Tweet,
                                                   schema_registry_client,
                                                   {'use.deprecated.format': False}),
            Topics.UsersTopic: ProtobufSerializer(twitter_pb2.User,
                                                  schema_registry_client,
                                                  {'use.deprecated.format': False}),
            Topics.CommentsTopic: ProtobufSerializer(twitter_pb2.Comment,
                                                     schema_registry_client,
                                                     {'use.deprecated.format': False}),
            Topics.TweetLikesTopic: ProtobufSerializer(twitter_pb2.TweetLike,
                                                       schema_registry_client,
                                                       {'use.deprecated.format': False}),
            Topics.UserFollowsTopic: ProtobufSerializer(twitter_pb2.UserFollow,
                                                        schema_registry_client,
                                                        {'use.deprecated.format': False}),
        }

        return serializers

    @staticmethod
    def _delivery_report(err, msg):
        """
        Reports the failure or success of a message delivery.
        Args:
            err (KafkaError): The error that occurred (None on success).
            msg (Message): The message that was produced or failed.
        """

        if err is not None:
            print("Delivery failed for User record {}: {}".format(msg.key(), err))
            return
        print('User record {} successfully produced to {} [{}] at offset {}'.format(
            msg.key(), msg.topic(), msg.partition(), msg.offset()))
