import json

from google.oauth2 import id_token
from google.oauth2.credentials import Credentials
from google.auth.transport import requests
from fastapi import APIRouter, HTTPException
from requests import Request

from core.config import Config
from tokens.models import Token

router = APIRouter()


def get_token(request: Request):
    return request.cookies.get(Config.refresh_token_cookie)


def refresh_token_func(refresh_token, db, client_secrets_file=Config.client_secret_file):
    with open(client_secrets_file, "r") as file:
        client_secrets = json.load(file)
    client_id = client_secrets["web"]["client_id"]
    client_secret = client_secrets["web"]["client_secret"]
    token_url = client_secret['web']['token_uri']

    credentials = Credentials(
        None,
        client_id=client_id,
        client_secret=client_secret,
        refresh_token=refresh_token,
        token_uri=token_url
    )
    credentials.refresh(requests.Request())
    db.query(Token).filter(Token.refresh_token == refresh_token).update(
        {"token": credentials.token, "refresh_token": credentials.refresh_token})
    id_info = id_token.verify_oauth2_token(credentials.id_token, requests.Request(), clock_skew_in_seconds=1)
    return {'exp': credentials.expiry, 'id': id_info['sub'], 'refresh_token': credentials.refresh_token}
