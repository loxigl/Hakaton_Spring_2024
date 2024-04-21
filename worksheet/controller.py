from datetime import datetime, timedelta

from fastapi import Depends, HTTPException

from core.session_maker import get_db
from login.controller import get_current_user, get_current_user_safe
from worksheet.dto import WorksheetCreateDTO, WorksheetDTO
from worksheet.models import Worksheet


def get_worksheet(user_id, db):
    worksheet = db.query(Worksheet).filter(Worksheet.user_id == user_id).first()
    if worksheet is None:
        raise HTTPException(status_code=404, detail="Worksheet not found")
    return worksheet


def create_worksheet(user_id, worksheet: WorksheetCreateDTO, db):
    worksheet = Worksheet(**worksheet.dict(), user_id=user_id)
    try:
        db_worksheet = db.query(Worksheet).filter(Worksheet.user_id == user_id).first()
        if db_worksheet is not None:
            raise HTTPException(status_code=400, detail="Worksheet already exists")
    except Exception:
        pass
    db.add(worksheet)
    db.commit()
    db.refresh(worksheet)
    return worksheet


def update_worksheet(user_id, worksheet: WorksheetDTO, db):
    db_worksheet = db.query(Worksheet).filter(Worksheet.user_id == user_id).first()
    if db_worksheet is None:
        raise HTTPException(status_code=404, detail="Worksheet not found")
    for key, value in worksheet.dict().items():
        setattr(db_worksheet, key, value)
    db.commit()
    db.refresh(db_worksheet)
    return db_worksheet


def delete_worksheet(user_id, db):
    worksheet = db.query(Worksheet).filter(Worksheet.user_id == user_id).first()
    if worksheet is None:
        raise HTTPException(status_code=404, detail="Worksheet not found")
    db.delete(worksheet)
    db.commit()
    return {"detail": "Worksheet deleted"}


def check_last_meeting_time(current_user=Depends(get_current_user_safe)):
    if not current_user:
        return
    last_meeting_time = current_user.worksheet.chosen_datetime

    if datetime.now() - last_meeting_time >= timedelta(hours=3):
        raise HTTPException(status_code=307, detail="Redirect to survey", headers={"Location": "/survey"})
