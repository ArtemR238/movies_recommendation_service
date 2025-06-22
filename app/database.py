from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

db_url = "postgresql://postgres:postgres@db:5432/moviedb"
engine = create_engine(db_url, future=True, pool_pre_ping=True, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
