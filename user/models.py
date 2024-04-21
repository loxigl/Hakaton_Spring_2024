from core.db_base import Base

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    username = Column(String)
    email = Column(String)
    given_name = Column(String)
    family_name = Column(String)
    photo_url = Column(String)

    worksheet = relationship("Worksheet", uselist=False, back_populates="user")
    token = relationship("Token", uselist=False, back_populates="user")


class Token(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    token = Column(String, index=True)
    refresh_token = Column(String, index=True)
    user = relationship("User", back_populates="token")
