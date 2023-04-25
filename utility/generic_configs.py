# This package contains configurations that are used across the project, including both producer and consumer.

from dataclasses import dataclass


@dataclass
class Topics:
    TweetsTopic: str = "Model.Tweets.1"
    UsersTopic: str = "Model.Users.1"
    CommentsTopic: str = "Model.Comments.1"
    TweetLikesTopic: str = "Model.TweetLikes.1"
    UserFollowsTopic: str = "Model.UserFollows.1"


# Dictionary of topics and their producing probability.
TOPICS_TO_PRODUCING_PROBABILITY = {
    Topics.TweetsTopic: 0.3,
    Topics.UsersTopic: 0.2,
    Topics.CommentsTopic: 0.2,
    Topics.TweetLikesTopic: 0.1,
    Topics.UserFollowsTopic: 0.1,
}
