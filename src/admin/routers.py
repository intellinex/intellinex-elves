from fastapi import APIRouter
from src.admin.routes import dashboard
from src.admin.routes import user
from src.admin.routes import notification
from src.admin.routes import profile
from src.admin.routes import platform
from src.admin.routes import channel
from src.admin.routes import product
from src.admin.routes import order

from src.admin.routes import transaction

app_router = APIRouter()

app_router.include_router(router=dashboard.router, prefix="/admin")
app_router.include_router(router=user.router, prefix="/user")
app_router.include_router(router=notification.router, prefix="/notification")
app_router.include_router(router=profile.router, prefix="/profile")
app_router.include_router(router=platform.router, prefix="/platform")
app_router.include_router(router=channel.router, prefix="/channel")
app_router.include_router(router=product.router, prefix="/product")
app_router.include_router(router=order.router, prefix="/order")
app_router.include_router(router=transaction.router, prefix="/transaction")
