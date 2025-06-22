import csv
from sqlalchemy import text
from .database import SessionLocal, engine, Base
from . import models


def reset_schema():
    print("Dropping & recreating schema, and creating tables…")
    with engine.begin() as conn:
        conn.execute(text("DROP SCHEMA IF EXISTS public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))
        Base.metadata.create_all(bind=conn)
    print("Schema reset complete.")


def load_movies(path: str):
    session = SessionLocal()
    try:
        print("Loading movies…")
        with open(path, encoding="utf8") as f:
            for row in csv.DictReader(f):
                session.add(
                    models.Movie(
                        id=int(row["movieId"]),
                        title=row["title"],
                    )
                )
        session.commit()
    finally:
        session.close()


def load_users(ratings_path: str):
    session = SessionLocal()
    try:
        print("Loading users…")
        user_ids = {int(r["userId"]) for r in csv.DictReader(open(ratings_path, encoding="utf8"))}
        for uid in sorted(user_ids):
            session.add(models.User(id=uid, username=f"user{uid}"))
        session.commit()
    finally:
        session.close()


def load_ratings(path: str):
    session = SessionLocal()
    try:
        print("Loading ratings…")
        with open(path, encoding="utf8") as f:
            for row in csv.DictReader(f):
                session.add(
                    models.Rating(
                        user_id=int(row["userId"]),
                        movie_id=int(row["movieId"]),
                        rating=int(float(row["rating"])),
                    )
                )
        session.commit()
    finally:
        session.close()


if __name__ == "__main__":
    BASE = "/app/data/ml-latest-small"
    reset_schema()
    load_movies(f"{BASE}/movies.csv")
    load_users(f"{BASE}/ratings.csv")
    load_ratings(f"{BASE}/ratings.csv")
    print("Full import complete.")
