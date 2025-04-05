from fastapi import APIRouter
from src.api.v1.endpoint import index

api_router = APIRouter() # This must come FIRST
api_router.include_router(index.router, tags=["Initializations"])