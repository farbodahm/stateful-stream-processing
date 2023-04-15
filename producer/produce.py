from model import twitter_pb2
import datetime
import argparse
from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer
from time import sleep

mesg = twitter_pb2.Tweet(text="Happy", user_id="farbod", tweet_id="12")
mesg.tweeted_date.FromDatetime(datetime.datetime.now())

print(mesg)


def delivery_report(err, msg):
    """
    Reports the failure or success of a message delivery.
    Args:
        err (KafkaError): The error that occurred on None on success.
        msg (Message): The message that was produced or failed.
    """

    if err is not None:
        print("Delivery failed for User record {}: {}".format(msg.key(), err))
        return
    print('User record {} successfully produced to {} [{}] at offset {}'.format(
        msg.key(), msg.topic(), msg.partition(), msg.offset()))


def main(args: argparse.Namespace) -> None:
    """Main Function"""
    topic = args.topic

    schema_registry_conf = {'url': args.schema_registry}
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    string_serializer = StringSerializer('utf8')
    protobuf_serializer = ProtobufSerializer(twitter_pb2.Tweet,
                                             schema_registry_client,
                                             {'use.deprecated.format': False})

    producer_conf = {'bootstrap.servers': args.bootstrap_servers,
                     'receive.message.max.bytes': 1500000000,
                     }

    producer = Producer(producer_conf)

    print("Producing user records to topic {}. ^C to exit.".format(topic))

    # Serve on_delivery callbacks from previous calls to produce()
    producer.poll(0.0)
    try:
        producer.produce(topic=topic, partition=0,
                         key=string_serializer("test2"),
                         value=protobuf_serializer(
                             mesg, SerializationContext(topic, MessageField.VALUE)),
                         on_delivery=delivery_report)
        sleep(2)
    except Exception as e:
        print("Shit", e)
        raise e

    print("\nFlushing records...")
    producer.flush()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="ProtobufSerializer example")
    parser.add_argument('-b', dest="bootstrap_servers", required=True,
                        help="Bootstrap broker(s) (host[:port])")
    parser.add_argument('-s', dest="schema_registry", required=True,
                        help="Schema Registry (http(s)://host[:port]")
    parser.add_argument('-t', dest="topic", default="example_serde_protobuf",
                        help="Topic name")

    main(parser.parse_args())
