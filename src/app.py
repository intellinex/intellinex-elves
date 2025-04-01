from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.db.mongodb import close_mongo_connection, connect_to_mongo
from src.core.config import settings
from src.util.middleware import AuthMiddleware

from src.api.v1.routes import api_router


app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)
app.add_middleware(AuthMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API ROUTERS
app.include_router(api_router, prefix="/api/v1")


# START UP AND SHUTDOWN DATABASE
@app.on_event("startup")
async def startup():
    """Connect to MongoDB on startup."""
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown():
    """Close MongoDB connection on shutdown."""
    await close_mongo_connection()
