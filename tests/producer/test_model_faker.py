from datetime import datetime

import pytest
from faker import Faker

from producer.model_faker import FakeDataModel
from utility.exceptions import UserNotFoundError, TweetNotFoundError

# NOTE: Changing this value will change the result of each test; So tests may fail if you change this
FAKER_SEED_VALUE = 0

SAMPLE_TEXTS = ["sample text 1", "sample text 2"]


@pytest.fixture
def fake_data_model() -> FakeDataModel:
    """Create FakeDataModel with a static seed to generate same result on each run"""
    faker = Faker()
    faker.seed_instance(FAKER_SEED_VALUE)

    return FakeDataModel(faker=faker)


@pytest.fixture
def fake_data_model_with_texts() -> FakeDataModel:
    """Create FakeDataModel with previously given texts"""
    faker = Faker()
    faker.seed_instance(FAKER_SEED_VALUE)

    return FakeDataModel(faker=faker, texts=SAMPLE_TEXTS)


def test_generate_user_model_succedes(fake_data_model: FakeDataModel):
    user = fake_data_model.generate_user_model()

    assert user.id == "1654615998"
    assert user.first_name == "Katherine"
    assert user.last_name == "Fisher"
    assert user.email == "tammy76@example.com"
    assert type(user.created_date.ToDatetime()) is datetime


def test_generate_tweet_model_without_user_raises_exception(
    fake_data_model: FakeDataModel,
):
    with pytest.raises(UserNotFoundError):
        fake_data_model.generate_tweet_model()


def test_generate_tweet_model_succedes(
    fake_data_model: FakeDataModel,
):
    user = fake_data_model.generate_user_model()
    tweet = fake_data_model.generate_tweet_model()

    assert tweet.id == "1235478542"
    assert tweet.user_id == user.id
    assert tweet.text == (
        "On traditional measure example sense peace. "
        "Would mouth relate own chair. Role together range line.\n"
        "Its particularly tree whom local tend. Artist truth trouble behavior style."
    )
    assert type(tweet.tweeted_date.ToDatetime()) is datetime


def test_generate_comment_model_without_user_raises_exception(
    fake_data_model: FakeDataModel,
):
    with pytest.raises(UserNotFoundError):
        fake_data_model.generate_comment_model()


def test_generate_comment_model_without_tweet_raises_exception(
    fake_data_model: FakeDataModel,
):
    fake_data_model.generate_user_model()
    with pytest.raises(TweetNotFoundError):
        fake_data_model.generate_comment_model()


def test_generate_comment_model_succedes(
    fake_data_model: FakeDataModel,
):
    user = fake_data_model.generate_user_model()
    tweet = fake_data_model.generate_tweet_model()
    comment = fake_data_model.generate_comment_model()

    assert comment.id == "141615452"
    assert comment.tweet_id == tweet.id
    assert comment.user_id == user.id
    assert comment.text == "Before something first drug contain start."
    assert type(comment.commented_date.ToDatetime()) is datetime


def test_generate_tweetlike_model_without_user_raises_exception(
    fake_data_model: FakeDataModel,
):
    with pytest.raises(UserNotFoundError):
        fake_data_model.generate_tweetlike_model()


def test_generate_tweetlike_model_without_tweet_raises_exception(
    fake_data_model: FakeDataModel,
):
    fake_data_model.generate_user_model()
    with pytest.raises(TweetNotFoundError):
        fake_data_model.generate_tweetlike_model()


def test_generate_tweetlike_model_succedes(
    fake_data_model: FakeDataModel,
):
    user = fake_data_model.generate_user_model()
    tweet = fake_data_model.generate_tweet_model()
    tweet_like = fake_data_model.generate_tweetlike_model()

    assert tweet_like.id == "1911213317"
    assert tweet_like.tweet_id == tweet.id
    assert tweet_like.user_id == user.id
    assert type(tweet_like.liked_date.ToDatetime()) is datetime


def test_generate_userfollow_model_without_user_raises_exception(
    fake_data_model: FakeDataModel,
):
    with pytest.raises(UserNotFoundError):
        fake_data_model.generate_userfollow_model()


def test_generate_userfollow_model_without_two_users_raises_exception(
    fake_data_model: FakeDataModel,
):
    fake_data_model.generate_user_model()

    with pytest.raises(UserNotFoundError):
        fake_data_model.generate_userfollow_model()


def test_generate_userfollow_model_succedes(
    fake_data_model: FakeDataModel,
):
    user1 = fake_data_model.generate_user_model()
    user2 = fake_data_model.generate_user_model()
    user_follow = fake_data_model.generate_userfollow_model()

    user_ids = [user1.id, user2.id]
    follower_id = user_follow.follower_id
    assert follower_id in user_ids
    user_ids.remove(follower_id)

    assert user_follow.followed_id in user_ids
    assert type(user_follow.followed_date.ToDatetime()) is datetime


def test_generate_tweet_model_with_previously_given_text_succedes(
    fake_data_model_with_texts: FakeDataModel,
):
    fake_data_model_with_texts.generate_user_model()
    tweet = fake_data_model_with_texts.generate_tweet_model()

    assert tweet.text in SAMPLE_TEXTS


def test_generate_comment_model_with_previously_given_text_succedes(
    fake_data_model_with_texts: FakeDataModel,
):
    fake_data_model_with_texts.generate_user_model()
    fake_data_model_with_texts.generate_tweet_model()
    comment = fake_data_model_with_texts.generate_comment_model()

    assert comment.text in SAMPLE_TEXTS
