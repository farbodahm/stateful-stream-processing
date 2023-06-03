"""This package will generate random data (with model type) using Faker."""

from faker import Faker
from typing import List, Optional
import random
import datetime

from model import twitter_pb2
from utility.logger import logger
from utility.exceptions import UserNotFoundError, TweetNotFoundError


class FakeDataModel:
    """Generate fake models to further produce them in Kafka topics."""

    ID_MAX_INT = 2147483647

    def __init__(self, texts: Optional[List[str]] = None) -> None:
        self._faker = Faker()
        self._texts = texts

        # List of all of the generated tweet ids so far
        self._generated_tweet_ids: List[str] = []
        # List of all of the generated user ids so far
        self._generated_user_ids: List[str] = []
        # List of all of the generated comment ids so far
        self._generated_comment_ids: List[str] = []

    def generate_tweet_model(self) -> twitter_pb2.Tweet:
        """Return a new generated fake Tweet model"""
        if len(self._generated_user_ids) == 0:
            logger.error(
                "No users are created. First you need to create a User "
                "before creating a new Tweet."
            )
            raise UserNotFoundError("There aren't any users created")

        text = self._faker.text() if self._texts is None else random.choice(self._texts)

        tweet = twitter_pb2.Tweet(
            id=self._generate_new_tweet_id(),
            user_id=random.choice(self._generated_user_ids),
            text=text,
        )
        tweet.tweeted_date.FromDatetime(datetime.datetime.now())

        return tweet

    def generate_user_model(self) -> twitter_pb2.User:
        """Return a new generated fake User model"""
        user = twitter_pb2.User(
            id=self._generate_new_user_id(),
            first_name=self._faker.first_name(),
            last_name=self._faker.last_name(),
            email=self._faker.email(),
            gender=random.choice(
                [twitter_pb2.User.Gender.FEMALE, twitter_pb2.User.Gender.MALE]
            ),
        )
        user.created_date.FromDatetime(datetime.datetime.now())

        return user

    def generate_tweetlike_model(self) -> twitter_pb2.TweetLike:
        """Return a new generated fake TweetLike model.
        This class, models a Tweet liked by a User."""
        if len(self._generated_user_ids) == 0:
            logger.error(
                "No users are created. First you need to create a User "
                "before creating a new TweetLike."
            )
            raise UserNotFoundError("There aren't any users created")

        if len(self._generated_tweet_ids) == 0:
            logger.error(
                "No tweets are created. First you need to create a Tweet "
                "before creating a new TweetLike."
            )
            raise TweetNotFoundError("There aren't any tweets created")

        tweetlike = twitter_pb2.TweetLike(
            id=str(self._faker.unique.random_int(max=FakeDataModel.ID_MAX_INT)),
            tweet_id=random.choice(self._generated_tweet_ids),
            user_id=random.choice(self._generated_user_ids),
        )
        tweetlike.liked_date.FromDatetime(datetime.datetime.now())

        return tweetlike

    def generate_comment_model(self) -> twitter_pb2.Comment:
        """Return a new generated fake Comment model.
        This class, models a Comment made by a User on a Tweet."""
        if len(self._generated_user_ids) == 0:
            logger.error(
                "No users are created. First you need to create a User "
                "before creating a new Comment."
            )
            raise UserNotFoundError("There aren't any users created")

        if len(self._generated_tweet_ids) == 0:
            logger.error(
                "No tweets are created. First you need to create a Tweet "
                "before creating a new Comment."
            )
            raise TweetNotFoundError("There aren't any tweets created")

        text = (
            self._faker.sentence()
            if self._texts is None
            else random.choice(self._texts)
        )

        comment = twitter_pb2.Comment(
            id=self._generate_new_comment_id(),
            tweet_id=random.choice(self._generated_tweet_ids),
            user_id=random.choice(self._generated_user_ids),
            text=text,
        )
        comment.commented_date.FromDatetime(datetime.datetime.now())

        return comment

    def generate_userfollow_model(self) -> twitter_pb2.UserFollow:
        """Return a new generated fake UserFollow model.
        This class, models a User following another User."""
        if len(self._generated_user_ids) < 2:
            logger.error(
                "You need more than 2 users to model a follow. "
                "First call creating User model 2 times."
            )
            raise UserNotFoundError("You need more than 2 users to model a follow")

        # One user can not follow him/her self
        followed_id = random.choice(self._generated_user_ids)
        follower_id = random.choice(self._generated_user_ids)
        while follower_id == followed_id:
            follower_id = random.choice(self._generated_user_ids)

        userfollow = twitter_pb2.UserFollow(
            id=str(self._faker.unique.random_int(max=FakeDataModel.ID_MAX_INT)),
            followed_id=followed_id,
            follower_id=follower_id,
        )
        userfollow.followed_date.FromDatetime(datetime.datetime.now())

        return userfollow

    def _generate_new_tweet_id(self) -> str:
        """Generate a new Tweet id and add that to the list of generated
        Tweet ids"""
        new_id = str(self._faker.unique.random_int(max=FakeDataModel.ID_MAX_INT))
        self._generated_tweet_ids.append(new_id)

        return new_id

    def _generate_new_user_id(self) -> str:
        """Generate a new User id and add that to the list of generated
        User ids"""
        new_id = str(self._faker.unique.random_int(max=FakeDataModel.ID_MAX_INT))
        self._generated_user_ids.append(new_id)

        return new_id

    def _generate_new_comment_id(self) -> str:
        """Generate a new Comment id and add that to the list of generated
        Comment ids"""
        new_id = str(self._faker.unique.random_int(max=FakeDataModel.ID_MAX_INT))
        self._generated_comment_ids.append(new_id)

        return new_id
