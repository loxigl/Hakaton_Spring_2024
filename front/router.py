from datetime import datetime

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from starlette.responses import RedirectResponse

from core.session_maker import get_db
from core.template_base import templates
from login.controller import get_current_user, get_current_user_safe
from user.random_alghoritms import get_users_with_similar_meetings

router = APIRouter()


@router.get("/")
def index(request: Request, current_user=Depends(get_current_user_safe)):
    return templates.TemplateResponse("/main_page/index.html", {"request": request, "current_user": current_user})


@router.get("/worksheet")
def worksheet(request: Request, current_user=Depends(get_current_user_safe)):
    if not current_user:
        return RedirectResponse(url="/api/v1/login")
    return templates.TemplateResponse("/worksheet/worksheet.html", {"request": request, "current_user": current_user})


@router.get("/survey")
def survey(request: Request, current_user=Depends(get_current_user_safe)):
    if not current_user:
        return RedirectResponse(url="/api/v1/login")
    return templates.TemplateResponse("/survey/opros.html", {"request": request, "current_user": current_user})


def is_weekend():
    today = datetime.today().weekday()
    return today == 5 or today == 6


from datetime import datetime, timedelta


def get_next_weekend():
    today = datetime.today()

    day_of_week = today.weekday()
    if day_of_week < 5:
        next_saturday = today + timedelta(days=(5 - day_of_week))
        return next_saturday.strftime("%d.%m.%y")
    elif day_of_week == 5 or day_of_week == 6:
        return today.strftime("%d.%m.%y")


@router.get('/partners')
def partners(request: Request, current_user=Depends(get_current_user_safe), db=Depends(get_db)):
    partner = []
    if not current_user:
        return RedirectResponse(url="/api/v1/login")
    if not current_user.worksheet:
        return RedirectResponse(url="/api/v1/worksheet")
    if is_weekend():
        partner = get_users_with_similar_meetings(current_user=current_user, db=db)
    return templates.TemplateResponse("/partners/base.html",
                                      {"request": request, "current_user": current_user, 'today': is_weekend(),
                                       'partner': partner, 'next_weekend': get_next_weekend()})
