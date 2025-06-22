from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter()


@router.get("", response_model=list[schemas.MovieOut])
def list_movies(
    search: str = Query(None, description="Optional search substring for movie title"),
    db: Session = Depends(get_db),
):
    query = db.query(models.Movie)
    if search:
        query = query.filter(models.Movie.title.ilike(f"%{search}%"))
    movies = query.all()
    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")
    return movies
