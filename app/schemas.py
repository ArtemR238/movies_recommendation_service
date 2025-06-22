from pydantic import BaseModel, conint
from datetime import datetime


class MovieBase(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True


class MovieOut(MovieBase):
    avg_rating: float | None = None


class RatingInput(BaseModel):
    user_id: int
    movie_id: int
    rating: conint(ge=1, le=5)


class RatingOut(BaseModel):
    user_id: int
    movie_id: int
    rating: int
    timestamp: datetime

    class Config:
        from_attributes = True


class RecommendationList(BaseModel):
    user_id: int
    recommendations: list[MovieOut]
