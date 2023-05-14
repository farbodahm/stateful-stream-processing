import argparse

# Protobuf generated class; resides at ./protobuf/user_pb2.py
from model import twitter_pb2
from confluent_kafka import Consumer
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry.protobuf import ProtobufDeserializer


def main(args: argparse.Namespace) -> None:
    topic = args.topic

    protobuf_deserializer = ProtobufDeserializer(twitter_pb2.Tweet,
                                                 {'use.deprecated.format': False})

    consumer_conf = {'bootstrap.servers': args.bootstrap_servers,
                     'group.id': args.group,
                     'auto.offset.reset': "earliest",
                     'enable.auto.commit': False, }

    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic])

    while True:
        try:
            # SIGINT can't be handled when polling, limit timeout to 1 second.
            msg = consumer.poll(1.0)
            if msg is None:
                continue

            tweet = protobuf_deserializer(
                msg.value(), SerializationContext(topic, MessageField.VALUE))

            if tweet is not None:
                print(tweet)
        except KeyboardInterrupt:
            break

    consumer.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="ProtobufDeserializer example")
    parser.add_argument('-b', dest="bootstrap_servers", required=True,
                        help="Bootstrap broker(s) (host[:port])")
    parser.add_argument('-s', dest="schema_registry", required=True,
                        help="Schema Registry (http(s)://host[:port]")
    parser.add_argument('-t', dest="topic", default="example_serde_protobuf",
                        help="Topic name")
    parser.add_argument('-g', dest="group", default="example_serde_protobuf",
                        help="Consumer group")

    main(parser.parse_args())
