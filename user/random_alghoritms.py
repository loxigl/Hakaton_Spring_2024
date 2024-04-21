from operator import itemgetter

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from core.session_maker import get_db
from login.controller import get_current_user
from user.models import User
from worksheet.models import Worksheet

router = APIRouter()


@router.get("/users_with_similar_meetings/")
def get_users_with_similar_meetings(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    user = current_user
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_worksheet = user.worksheet
    if user_worksheet is None:
        raise HTTPException(status_code=404, detail="User worksheet not found")

    user_meeting_time = user_worksheet.chosen_datetime
    current_user_hobbies = user_worksheet.hobby

    users = db.query(User).join(Worksheet).filter(
        Worksheet.chosen_datetime.between(user_meeting_time - timedelta(hours=1),
                                          user_meeting_time + timedelta(hours=1)), User.id != user.id).all()

    users_with_hobbies = []
    for user in users:
        user_hobbies = user.worksheet.hobby
        matching_hobbies_count = len(set(user_hobbies) & set(current_user_hobbies))
        user_dict = user.__dict__
        user_dict['matching_hobbies_count'] = matching_hobbies_count
        users_with_hobbies.append(user_dict)

    users_with_hobbies.sort(key=lambda x: x['matching_hobbies_count'], reverse=True)

    return users_with_hobbies
