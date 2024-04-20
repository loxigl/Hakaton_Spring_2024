from fastapi import APIRouter, Depends
from google.auth.transport import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from starlette.responses import RedirectResponse

from core.config import Config
from core.session_maker import get_db
from user.controller import create_user, create_user_from_google_info, is_user_exists
from login.controller import create_access_token

router = APIRouter()


@router.get("/")
async def login():
    flow = Flow.from_client_secrets_file(
        client_secrets_file=Config.client_secret_file,
        scopes=Config.google_scopes,
        redirect_uri=Config.redirect_uri
    )
    authorization_url, state = flow.authorization_url(
        access_type="offline",
        prompt="consent"
    )
    return RedirectResponse(authorization_url)


@router.get("/callback")
async def callback(code: str, state: str, session=Depends(get_db)):
    flow = Flow.from_client_secrets_file(
        client_secrets_file=Config.client_secret_file,
        scopes=Config.google_scopes,
        redirect_uri=Config.redirect_uri
    )
    flow.fetch_token(code=code)
    credentials = flow.credentials

    id_info = id_token.verify_oauth2_token(credentials.id_token, requests.Request(), clock_skew_in_seconds=1)
    user = create_user_from_google_info(id_info)
    response = RedirectResponse(url="/worksheet")
    response.set_cookie(key=Config.user_cookie_key, value=create_access_token({'user_id': user.id}, id_info.get('exp')))
    if is_user_exists(user, session):
        return response
    create_user(user, session)
    return response
