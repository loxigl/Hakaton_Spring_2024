from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, ARRAY
from sqlalchemy.orm import relationship

from core.db_base import Base


class Worksheet(Base):
    __tablename__ = "worksheets"
    id = Column(Integer, primary_key=True)
    given_name = Column(String)
    family_name = Column(String)
    phone_number = Column(String)
    chosen_datetime = Column(DateTime)
    meeting_duration = Column(String)
    hobby = Column(ARRAY(String))
    user_id = Column(String, ForeignKey('users.id'))

    User = relationship("User", back_populates="Worksheet")
