from typing import List
from typing import Optional
from datetime import datetime
import enum

from sqlalchemy import ForeignKey, String, Enum, DateTime, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Gender(enum.Enum):
    FEMALE = 1
    MALE = 2


class Base(DeclarativeBase):
    pass


# tweet_like_association_table = Table(
#     "tweet_like",
#     Base.metadata,
#     Column("id", primary_key=True),
#     Column("user_id", ForeignKey("user.id")),
#     Column("tweet_id", ForeignKey("tweet.id")),
#     Column("liked_date", DateTime),
# )


class TweetLike(Base):
    __tablename__ = "tweet_like"

    id: Mapped[int] = mapped_column(primary_key=True)
    tweet_id: Mapped[int] = mapped_column(ForeignKey("tweet.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    liked_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(45))
    last_name: Mapped[str] = mapped_column(String(45))
    email: Mapped[str] = mapped_column(String(45))
    gender: Mapped[Gender] = mapped_column(Enum(Gender))
    created_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    # Relationships
    tweets: Mapped[List["Tweet"]] = relationship("Tweet", back_populates="user")
    liked_tweets: Mapped[List["Tweet"]] = relationship(
        secondary=TweetLike.__table__, back_populates="liked_by"
    )
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="user")


class Tweet(Base):
    __tablename__ = "tweet"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(255))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    tweeted_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="tweets")
    liked_by: Mapped[List["User"]] = relationship(
        secondary=TweetLike.__table__, back_populates="liked_tweets"
    )
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="tweet")


class Comment(Base):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    tweet_id: Mapped[int] = mapped_column(ForeignKey("tweet.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    text: Mapped[str] = mapped_column(String(255))
    commented_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="comments")
    tweet: Mapped["Tweet"] = relationship("Tweet", back_populates="comments")
