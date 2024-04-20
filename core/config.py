import os


class Config:
    user_cookie_key = 'user'
    worksheet_cookie_key = 'worksheet'
    reload = True
    secret_key = os.getenv("SECRET_KEY")
    algorithm = "HS256"
    db_connection_string = os.environ.get("DB_CONNECTION_STRING") or "sqlite:///./test.db"
    redirect_uri = os.environ.get("REDIRECT_URI") or "http://localhost:8099/login/callback"
    google_scopes = ["openid", "https://www.googleapis.com/auth/userinfo.profile",
                     "https://www.googleapis.com/auth/userinfo.email"]
    client_secret_file = os.environ.get("CLIENT_SECRET_FILE") or "client_secret.json"
    host = os.getenv("HOST", "localhost")
    port = os.getenv("PORT", 8099)
