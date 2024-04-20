from fastapi import HTTPException, Depends

from core.session_maker import get_db
from user.models import User


def create_user_from_google_info(user_info):
    user = User()
    user.id = user_info["sub"]
    user.username = user_info["email"]
    user.email = user_info["email"]
    user.given_name = user_info["given_name"]
    user.family_name = user_info["family_name"]
    user.photo_url = user_info["picture"]
    return user


def is_user_exists(user, db):
    _user = db.query(User).filter(User.id == user.id).first()
    if _user is None:
        return False
    return True


def create_user(user, db):
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as e:
        db.rollback()
        user = db.query(User).filter(User.id == user.id).first()
    return user


def get_user(user_id, db=Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
