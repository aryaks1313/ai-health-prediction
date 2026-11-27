from sqlalchemy import create_engine
from sqlalchemy.orm import (
    sessionmaker,
    DeclarativeBase
)

from app.config import DATABASE_URL

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()