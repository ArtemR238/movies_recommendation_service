from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Movie, Rating
from ..schemas import MovieOut, RecommendationList
from ..recommender import recommender_service

router = APIRouter()


@router.get("/{uid}/watched", response_model=list[MovieOut])
def watched(uid: int, db: Session = Depends(get_db)):
    if not db.get(User, uid):
        raise HTTPException(404, "User not found")
    return db.query(Movie).join(Rating).filter(Rating.user_id == uid).all()


@router.get("/{uid}/unwatched", response_model=list[MovieOut])
def unwatched(uid: int, db: Session = Depends(get_db)):
    if not db.get(User, uid):
        raise HTTPException(404, "User not found")
    seen = db.query(Rating.movie_id).filter(Rating.user_id == uid)
    return db.query(Movie).filter(~Movie.id.in_(seen)).all()


@router.get("/{uid}/recommendations", response_model=RecommendationList)
def recommendations(uid: int, n: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    if not db.get(User, uid):
        raise HTTPException(404, "User not found")
    try:
        recs = recommender_service.recommend_for_user(uid, N=n)
    except RuntimeError:
        raise HTTPException(503, "Model not trained")
    movies = db.query(Movie).filter(Movie.id.in_(recs)).all() if recs else []
    if movies:
        movies.sort(key=lambda m: recs.index(m.id))
    return {"user_id": uid, "recommendations": movies}
