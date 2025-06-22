from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from ..database import get_db
from ..models import User, Movie, Rating
from ..schemas import RatingInput, RatingOut

router = APIRouter()


@router.put("/ratings", response_model=RatingOut)
def upsert_rating(inp: RatingInput, db: Session = Depends(get_db)):
    user = db.get(User, inp.user_id)
    movie = db.get(Movie, inp.movie_id)
    if not user or not movie:
        raise HTTPException(404, "User or Movie not found")
    existing = db.get(Rating, (inp.user_id, inp.movie_id))
    if existing:
        existing.rating = inp.rating
        existing.timestamp = datetime.utcnow()
        rating = existing
    else:
        rating = Rating(user_id=inp.user_id, movie_id=inp.movie_id, rating=inp.rating)
        db.add(rating)
    db.commit()
    db.refresh(rating)
    return rating