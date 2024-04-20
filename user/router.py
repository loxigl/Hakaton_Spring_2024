from fastapi import APIRouter, Depends

from login.controller import get_current_user, get_user

router = APIRouter()


@router.get('/')
def _get_current_user(current_user=Depends(get_current_user)):
    return current_user


@router.get('/id/')
def get_current_user_id(current_user=Depends(get_current_user)):
    return {'user_id': current_user.id}
