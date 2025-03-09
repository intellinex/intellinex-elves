from fastapi import APIRouter
from src.admin.routes import (
 dashboard
)


app_router = APIRouter()

app_router.include_router(router=dashboard.router, prefix="/admin")
