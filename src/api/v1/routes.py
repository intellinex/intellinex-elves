from fastapi import APIRouter
from src.api.v1.endpoint import index
# from bin import (
#     user
# )

api_router = APIRouter()

# api_router.include_router(user.router, prefix="/auth", tags=['User'])
api_router.include_router(index.router, tags=["Initializations"])