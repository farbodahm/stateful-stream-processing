"""This package will generate random data (with model type) using Faker."""

from faker import Faker
from typing import List
import random
import datetime

from model import twitter_pb2
from logger import logging
from exceptions import UserNotFoundError


class FakeDataModel:
    """Generate fake model to further produce them in Kafka topics."""
    ID_MAX_INT = 2147483647

    def __init__(self) -> None:
        self._faker = Faker()

        # List of all of the generated tweet ids
        self._generated_tweet_ids: List[str] = []
        # List of all of the generated user ids
        self._generated_user_ids: List[str] = []

    def generate_tweet_model(self) -> twitter_pb2.Tweet:
        """Return a new generated fake Tweet model"""
        if len(self._generated_user_ids) == 0:
            logging.error(
                "No users are created. First you need to create a User "
                "before creating a new Tweet.")
            raise UserNotFoundError("There aren't any users created")

        tweet = twitter_pb2.Tweet(
            tweet_id=self._generate_new_tweet_id(),
            user_id=random.choice(self._generated_user_ids),
            text=self._faker.text()
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
                [twitter_pb2.User.Gender.FEMALE, twitter_pb2.User.Gender.MALE])
        )
        user.created_date.FromDatetime(datetime.datetime.now())

        return user

    def _generate_new_tweet_id(self) -> str:
        """Generate a new Tweet id and add that to the list of generated
        Tweet ids"""
        new_id = str(self._faker.unique.random_int(
            max=FakeDataModel.ID_MAX_INT))
        self._generated_tweet_ids.append(new_id)

        return new_id

    def _generate_new_user_id(self) -> str:
        """Generate a new User id and add that to the list of generated
        User ids"""
        new_id = str(self._faker.unique.random_int(
            max=FakeDataModel.ID_MAX_INT))
        self._generated_user_ids.append(new_id)

        return new_id
