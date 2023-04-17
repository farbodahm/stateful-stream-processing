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

    def __init__(self) -> None:
        self._faker = Faker()

        # List of all of the generated tweet ids
        self._generated_tweet_ids: List[str] = []
        # List of all of the generated user ids
        self._generated_user_ids: List[str] = []

    def generate_tweet_model(self) -> twitter_pb2.Tweet:
        """Return a new generate fake Tweet model"""
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

    def _generate_new_tweet_id(self) -> str:
        """Generate a new Tweet id and add that to the list of generate
        Tweet ids"""
        new_id = self._faker.unique.random_int(max=2147483647)
        self._generated_tweet_ids.append(new_id)

        return new_id
