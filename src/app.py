from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from src.db.mongodb import close_mongo_connection, connect_to_mongo
from src.core.config import settings
from src.util.middleware import AuthMiddleware

from src.api.v1.routes import api_router
from src.admin.routers import app_router


app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(AuthMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

# API ROUTERS
app.include_router(api_router, prefix="/api/v1")

# APP ROUTERS (BACK-END)
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request":request})
app.include_router(router=app_router)

# START UP AND SHUTDOWN DATABASE
@app.on_event("startup")
async def startup():
    """Connect to MongoDB on startup."""
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown():
    """Close MongoDB connection on shutdown."""
    await close_mongo_connection()
