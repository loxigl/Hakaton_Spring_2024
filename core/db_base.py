import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from core.config import Config

Base = declarative_base()
createEngine = create_engine(Config.db_connection_string, pool_pre_ping=True, pool_size=20, max_overflow=0,
                             pool_recycle=3600)
