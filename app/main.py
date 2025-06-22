from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from threading import Thread

from .models import Rating
from .recommender import recommender_service
from .database import SessionLocal
from .routers import movies, users, ratings, retrain

app = FastAPI(title="MovieLens ALS Recommendation API")


@app.on_event("startup")
def startup_event():
    with SessionLocal() as db:
        if db.query(Rating).first():
            Thread(target=recommender_service.train, daemon=True).start()


@app.get("/", include_in_schema=False)
def docs_redirect():
    return RedirectResponse("/docs")


app.include_router(movies.router, prefix="/movies", tags=["Movies"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(ratings.router, tags=["Ratings"])
app.include_router(retrain.router, tags=["Admin"])
