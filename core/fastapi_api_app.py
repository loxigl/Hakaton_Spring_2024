from fastapi import FastAPI

from front.router import router as front_router
from worksheet.router import router as worksheet_router
from login.router import router as login_router

app = FastAPI()

app.include_router(worksheet_router, tags=["worksheet"], prefix="/worksheet")
app.include_router(login_router, tags=["login"], prefix="/login")


@app.get('/create_db')
def create_db():
    from core.database import create_tables
    create_tables()
    return {"message": "Database created"}


@app.get('/drop_db')
def drop_db():
    from core.database import drop_tables
    drop_tables()
    return {"message": "Database dropped"}
