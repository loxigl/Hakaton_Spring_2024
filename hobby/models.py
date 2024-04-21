from core.db_base import Base
from sqlalchemy import Column, Integer, String


class Hobby(Base):
    __tablename__ = 'hobby'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
