from typing import Dict, Callable, List
from copy import deepcopy

from sqlalchemy.orm import Session
from google.protobuf.message import Message
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

from model import twitter_pb2
from model.twitter_database_model import (
    Base,
    User,
    Gender,
    Tweet,
    TweetLike,
    Comment,
    UserFollow,
)
from utility.generic_configs import Topics
from utility.logger import logger
from utility.exceptions import ProtobufToORMTransformerNotFound


class DatabaseWriter:
    """Class for writing consumed Protobuf messages to database."""

    def __init__(
        self,
        db_session: Session,
        max_write_pool_buffer: int = 5,
    ) -> None:
        self.db_session = db_session

        self.topic_to_transformers = self._topic_to_transformer()

        # Maximum number of messages to be written to database in a single transaction.
        # This is to avoid database connection overload.
        self.max_write_pool_buffer = max_write_pool_buffer
        self._write_pool_buffer: List[Base] = []

        # A child record may be recieved faster than the parent record from Kafka
        # topics. So it will be failed to write to DB because of ForeignKey
        # constraint violation. We store it in a temp buffer and try to write it in next cycles.
        self._fk_constraint_failed_buffer: List[Base] = []

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
            logger.error(
                f"Error while transforming Protobuf message {message} to ORM model: {e}"
            )
            raise e
        self._write_pool_buffer.append(db_model)

        # TODO: Also flush buffer based on time schedules.
        if len(self._write_pool_buffer) >= self.max_write_pool_buffer:
            self._flush_write_pool()

    def _flush_write_pool(self) -> None:
        """Flush pool to database."""
        logger.info(
            f"Flushing write pool with {len(self._write_pool_buffer)} messages to database."
        )

        try:
            self.db_session.bulk_save_objects(self._write_pool_buffer)
            self.db_session.commit()
        except IntegrityError as e:
            # Parent record is not processed yet; Insert records into a temp buffer
            # and try to save later again.
            logger.warning(f"Forign ket violation: {e}")
            self.db_session.rollback()
            self._fk_constraint_failed_buffer += deepcopy(self._write_pool_buffer)
        except Exception as e:
            logger.error(f"Error while committing write pool to database: {e}")
            raise e
        else:
            logger.info("Successfully committed write pool to database")

        self._write_pool_buffer.clear()

        if len(self._fk_constraint_failed_buffer) > 0:
            self._flush_fk_constraint_failed_pool()

    def _flush_fk_constraint_failed_pool(self) -> None:
        """Flush list which contains records that failed to write to DB
        because of FK constraint failed error."""
        logger.info(
            f"Flushing FK constraint failed pool with {len(self._fk_constraint_failed_buffer)} records"
        )
        temp_backup_pool: List[Base] = []

        for record in self._fk_constraint_failed_buffer:
            self.db_session.add(record)
            try:
                self.db_session.commit()
            except IntegrityError as e:
                if isinstance(e.orig, UniqueViolation):
                    logger.warning(
                        f"{record} Unique Primary Key violation; Ignoring record..."
                    )
                    self.db_session.rollback()
                    continue
                # Parent record is not added yet, store it for next cycle.
                logger.warning(f"Failed to insert record again: {e}")
                self.db_session.rollback()
                temp_backup_pool.append(record)
            except Exception as e:
                logger.error(f"Error while committing backup pool to database: {e}")
                raise e

        self._fk_constraint_failed_buffer = temp_backup_pool
        logger.info(
            f"After flushing FK constraint failed pool: {len(self._fk_constraint_failed_buffer)}"
        )

    def _topic_to_transformer(self) -> Dict[str, Callable[[Message], Base]]:
        """Map each topic to its Protobuf to ORM model transformer."""

        transformers = {
            Topics.UsersTopic: self._transform_user_protobuf_to_db_model,
            Topics.TweetsTopic: self._transform_tweet_protobuf_to_db_model,
            Topics.TweetLikesTopic: self._transform_tweet_like_protobuf_to_db_model,
            Topics.CommentsTopic: self._transform_comment_protobuf_to_db_model,
            Topics.UserFollowsTopic: self._transform_user_follow_protobuf_to_db_model,
        }

        return transformers

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

    def _transform_tweet_protobuf_to_db_model(
        self, protobuf_message: twitter_pb2.Tweet
    ) -> User:
        """Transforms Protobuf Tweet message to related database model."""

        tweet = Tweet(
            id=int(protobuf_message.id),
            text=protobuf_message.text,
            user_id=int(protobuf_message.user_id),
            tweeted_date=protobuf_message.tweeted_date.ToDatetime(),
        )
        return tweet

    def _transform_tweet_like_protobuf_to_db_model(
        self, protobuf_message: twitter_pb2.TweetLike
    ) -> User:
        """Transforms Protobuf Tweet message to related database model."""

        tweet_like = TweetLike(
            id=int(protobuf_message.id),
            tweet_id=int(protobuf_message.tweet_id),
            user_id=int(protobuf_message.user_id),
            liked_date=protobuf_message.liked_date.ToDatetime(),
        )
        return tweet_like

    def _transform_comment_protobuf_to_db_model(
        self, protobuf_message: twitter_pb2.Comment
    ) -> User:
        """Transforms Protobuf Comment message to related database model."""

        comment = Comment(
            id=int(protobuf_message.id),
            tweet_id=int(protobuf_message.tweet_id),
            user_id=int(protobuf_message.user_id),
            text=protobuf_message.text,
            commented_date=protobuf_message.commented_date.ToDatetime(),
        )
        return comment

    def _transform_user_follow_protobuf_to_db_model(
        self, protobuf_message: twitter_pb2.UserFollow
    ) -> User:
        """Transforms Protobuf UserFollow message to related database model."""

        user_follow = UserFollow(
            id=int(protobuf_message.id),
            followed_id=int(protobuf_message.followed_id),
            follower_id=int(protobuf_message.follower_id),
            followed_date=protobuf_message.followed_date.ToDatetime(),
        )
        return user_follow
