from typing import List
from typing import Optional
from datetime import datetime
import enum

from sqlalchemy import ForeignKey, String, Enum, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Gender(enum.Enum):
    FEMALE = 1
    MALE = 2


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(45))
    last_name: Mapped[str] = mapped_column(String(45))
    email: Mapped[str] = mapped_column(String(45))
    gender: Mapped[Gender] = mapped_column(Enum(Gender))
    created_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)


#     addresses: Mapped[List["Address"]] = relationship(
#         back_populates="user", cascade="all, delete-orphan"
#     )


# class Address(Base):
#     __tablename__ = "address"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     email_address: Mapped[str]
#     user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
#     user: Mapped["User"] = relationship(back_populates="addresses")
