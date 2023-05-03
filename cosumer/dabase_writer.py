from typing import Dict, Callable, List

from sqlalchemy.orm import Session
from google.protobuf.message import Message

from model import twitter_pb2
from model.twitter_database_model import Base, User, Gender
from utility.generic_configs import Topics
from utility.logger import logging
from utility.exceptions import ProtobufToORMTransformerNotFound


class DatabaseWriter:
    """Class for writing consumed Protobuf messages to database."""

    def __init__(self, db_session: Session, max_write_pool_buffer: int = 5) -> None:
        self.db_session = db_session

        self.topic_to_transformers = self._topic_to_transformer()

        # Maximum number of messages to be written to database in a single transaction.
        # This is to avoid database connection overload.
        self.max_write_pool_buffer = max_write_pool_buffer
        self._write_pool_buffer: List[Base] = []

    def write_to_database(self, topic: str, message: Message) -> None:
        """Add Protobuf message to DB write pool and flush the write pool when threshold reached."""

        transformer = self.topic_to_transformers.get(topic, None)
        if transformer is None:
            raise ProtobufToORMTransformerNotFound(
                f"Protobuf to ORM transformer not found for topic {topic}."
            )

        try:
            db_model = transformer(message)
        except Exception as e:
            logging.error(
                f"Error while transforming Protobuf message {message} to ORM model: {e}"
            )
            raise e
        self._write_pool_buffer.append(db_model)

        # TODO: Also flush buffer based on time schedules.
        if len(self._write_pool_buffer) >= self.max_write_pool_buffer:
            self._flush_write_pool()

    def _flush_write_pool(self) -> None:
        """Flush pool to database."""
        logging.info(
            f"Flushing write pool with {len(self._write_pool_buffer)} messages to database."
        )
        self.db_session.add_all(self._write_pool_buffer)

        try:
            self.db_session.commit()
        except Exception as e:
            logging.error(f"Error while committing write pool to database: {e}")
            raise e

        self._write_pool_buffer.clear()

    def _transform_user_protobuf_to_db_model(
        self, protobuf_message: twitter_pb2.User
    ) -> User:
        """Transforms Protobuf User message to related database model."""

        gender = Gender.FEMALE if protobuf_message.gender == 0 else Gender.MALE
        user = User(
            id=int(protobuf_message.id),
            first_name=protobuf_message.first_name,
            last_name=protobuf_message.last_name,
            email=protobuf_message.email,
            gender=gender,
            created_date=protobuf_message.created_date.ToDatetime(),
        )
        return user

    def _topic_to_transformer(self) -> Dict[str, Callable[[Message], Base]]:
        """Map each topic to its Protobuf to ORM model transformer."""

        transformers = {
            Topics.UsersTopic: self._transform_user_protobuf_to_db_model,
        }

        return transformers
