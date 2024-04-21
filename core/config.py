import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    encryption_key = os.environ.get("ENCRYPTION_KEY")
    user_cookie_key = 'user'
    refresh_token_cookie = 'ref_token'
    reload = True
    secret_key = os.getenv("SECRET_KEY")
    algorithm = "HS256"
    db_connection_string = os.environ.get("DB_CONNECTION_STRING")
