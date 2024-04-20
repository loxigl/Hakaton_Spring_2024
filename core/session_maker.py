import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.db_base import createEngine as engine

load_dotenv()


def get_db_session():
    SessionLocal = sessionmaker(autoflush=False, bind=engine, expire_on_commit=False)
    return SessionLocal()


def get_db():
    db = get_db_session()
    try:
        yield db
    finally:
        db.close()
