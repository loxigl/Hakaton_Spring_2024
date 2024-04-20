from fastapi import Depends

from core.session_maker import get_db
from hobby.models import Hobby


def get_hobbies(db=Depends(get_db)):
    hobbies = db.query(Hobby).all()
    return hobbies


def set_hobby(hobby, db=Depends(get_db)):
    db.add(hobby)
    db.commit()
    db.refresh(hobby)
    return hobby
