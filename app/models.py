from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=False)
    username = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    ratings = relationship("Rating", back_populates="user")


class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True, autoincrement=False)
    title = Column(String, nullable=False)
    avg_rating = Column(Integer, nullable=True)

    ratings = relationship("Rating", back_populates="movie")


class Rating(Base):
    __tablename__ = "ratings"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True, autoincrement=False)
    movie_id = Column(Integer, ForeignKey("movies.id"), primary_key=True, autoincrement=False)
    rating = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="ratings")
    movie = relationship("Movie", back_populates="ratings")
