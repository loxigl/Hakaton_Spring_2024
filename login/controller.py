from datetime import timedelta, datetime
from typing import Optional

from fastapi import HTTPException, Depends
from jose import jwt, JWTError
from starlette.requests import Request

from core.config import Config
from core.session_maker import get_db
from user.controller import get_user

SECRET_KEY = Config.secret_key
ALGORITHM = Config.algorithm


def create_access_token(data: dict, expires: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires:
        expire = expires
    else:
        expire = datetime.utcnow() + timedelta(days=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_cookie(request: Request):
    return request.cookies.get(Config.user_cookie_key)


def get_current_user(token: Optional[str] = Depends(get_cookie), db=Depends(get_db)) -> dict:
    if not token:
        raise HTTPException(status_code=403, detail="Not authenticated")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

    except JWTError:
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials",
        )
    user = get_user(user_id, db)

    return user


def get_current_user_safe(token: Optional[str] = Depends(get_cookie), db=Depends(get_db)) -> dict:
    if not token:
        return None
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
    except JWTError:
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials",
        )
    user = get_user(user_id, db)
    return user
