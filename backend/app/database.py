from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import Settings

settings = Settings()

engine = create_engine(settings.DATABASE_URL, echo=True)

Session = sessionmaker(bind=engine, autocommit=False, expire_on_commit=False)

Base = declarative_base()

def get_db():
    db = Session()

    try:
        yield(db)
    finally:
        db.close()


db = Annotated[Session, Depends(get_db)]