from fastapi import Depends, HTTPException

from core.session_maker import get_db
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
