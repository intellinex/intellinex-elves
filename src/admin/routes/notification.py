from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("/pages/notification/index.html", {
        "request": request,
        "title": "Notification",
        "current_page": "notification"
    })
