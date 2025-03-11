from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("/pages/user/index.html", {
        "request": request,
        "title": "User",
        "current_page": "user",
        "description": "Create, update user resource."
    })

@router.get("/roles", response_class=HTMLResponse)
async def user_role(request: Request):
    """
    docstring
    """
    return templates.TemplateResponse("/pages/user/role.html", {
        "request": request,
        "title": "User Role",
        "current_page": "user",
        "description": "Create, update user resource."
    })