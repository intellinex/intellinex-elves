from fastapi import APIRouter
from src.admin.routes import dashboard
from src.admin.routes import user
from src.admin.routes import notification

app_router = APIRouter()

app_router.include_router(router=dashboard.router, prefix="/admin")
app_router.include_router(router=user.router, prefix="/user")
app_router.include_router(router=notification.router, prefix="/notification")
