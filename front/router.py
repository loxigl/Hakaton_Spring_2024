from fastapi import APIRouter, Depends
from fastapi.requests import Request
from starlette.responses import RedirectResponse

from core.template_base import templates
from login.controller import get_current_user, get_current_user_safe

router = APIRouter()


@router.get("/")
def index(request: Request, current_user=Depends(get_current_user_safe)):
    return templates.TemplateResponse("/main_page/index.html", {"request": request, "current_user": current_user})


@router.get("/worksheet")
def worksheet(request: Request, current_user=Depends(get_current_user_safe)):
    if not current_user:
        return RedirectResponse(url="/api/v1/login")
    return templates.TemplateResponse("/worksheet/worksheet.html", {"request": request, "current_user": current_user})
