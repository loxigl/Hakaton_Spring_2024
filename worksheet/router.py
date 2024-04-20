from fastapi import APIRouter, Depends

from worksheet.controller import get_worksheet, create_worksheet, update_worksheet, delete_worksheet
from core.session_maker import get_db
from worksheet.dto import WorksheetCreateDTO

router = APIRouter()


@router.get('/{user_id}')
def read_worksheet(user_id: int, db=Depends(get_db)):
    return get_worksheet(user_id, db)


@router.post('/{user_id}')
def create_new_worksheet(user_id: int, worksheet: WorksheetCreateDTO, db=Depends(get_db)):
    return create_worksheet(user_id, worksheet, db)


@router.put('/{user_id}')
def update_existing_worksheet(user_id: int, worksheet: WorksheetCreateDTO, db=Depends(get_db)):
    return update_worksheet(user_id, worksheet, db)


@router.delete('/{user_id}')
def delete_existing_worksheet(user_id: int, db=Depends(get_db)):
    return delete_worksheet(user_id, db)
