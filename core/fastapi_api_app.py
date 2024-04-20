from fastapi import FastAPI

from user.router import router as user_router
from worksheet.router import router as worksheet_router
from login.router import router as login_router

app = FastAPI()

app.include_router(worksheet_router, tags=["worksheet"], prefix="/worksheet")
app.include_router(login_router, tags=["login"], prefix="/login")
app.include_router(user_router, tags=["user"], prefix="/user")
