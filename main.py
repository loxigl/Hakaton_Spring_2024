from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles

from core.config import Config
from core.fastapi_api_app import app as api_app
from front.router import router as front_router

load_dotenv()
app = FastAPI()
app.mount("/static", app=StaticFiles(directory='front/static'), name="static")
app.mount("/api/v1", api_app)
app.mount("/", front_router)

if __name__ == "__main__":
    uvicorn.run('main:app', host=Config.host, port=Config.port, reload=Config.reload)
