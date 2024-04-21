from datetime import timedelta, datetime

from typing import Optional, Any

from fastapi import HTTPException, Depends
from jose import jwt, JWTError
from cryptography.fernet import Fernet
from fastapi.requests import Request
from starlette.responses import RedirectResponse, Response

from core.config import Config
from core.session_maker import get_db
from tokens.router import get_token, refresh_token_func

from user.controller import get_user

SECRET_KEY = Config.secret_key
ALGORITHM = Config.algorithm


def encrypt_refresh_token(token: str) -> str:
    cipher_suite = Fernet(Config.encryption_key)
    cipher_text = cipher_suite.encrypt(token.encode())
    return cipher_text.decode()


def decrypt_refresh_token(token: str) -> str:
    """
    Расшифровывает refresh token с использованием ключа шифрования
    """
    cipher_suite = Fernet(Config.encryption_key)
    plain_text = cipher_suite.decrypt(token.encode())
    return plain_text.decode()


def refresh_jwt_token(request: Request, db=Depends(get_db)):
    token = get_refresh_token_cookie(request)
    if token is None:
        raise HTTPException(status_code=404, detail="Token not found")

    expiry = refresh_token_func(Config.client_secret_file, token, db)

    access_token = create_access_token(
        data={"user_id": expiry['id']}, expires=expiry['exp']
    )
    response = Response()
    response.set_cookie(Config.user_cookie_key, value=access_token)
    return access_token


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


def get_refresh_token_cookie(request: Request):
    return decrypt_refresh_token(request.cookies.get(Config.refresh_token_cookie))


def get_current_user(request: Request, token: Optional[str] = Depends(get_cookie), db=Depends(get_db)) -> dict | Any:

    if not token:
        raise HTTPException(status_code=403, detail="Not authenticated")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

    except JWTError:

        refresh_jwt_token(request, db)
        return get_current_user(request)

    user = get_user(user_id, db)

    return user



def get_current_user_safe(request: Request, token: Optional[str] = Depends(get_cookie), db=Depends(get_db)) -> dict:

    if not token:
        return None
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
    except JWTError:

        refresh_jwt_token(request, db)
        return get_current_user(request)

    user = get_user(user_id, db)
    return user
