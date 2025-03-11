from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse
from src.db.mongodb import db_instance

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# GET: Return list of model
@router.get("/", response_class=HTMLResponse)
async def index(request: Request, page: int = Query(1, ge=1), limit: int = Query(10, ge=1)):

    skip = (page - 1) * limit
    result = await db_instance.db['order'].find().skip(skip).limit(limit).to_list(limit)
    total = await db_instance.db['order'].count_documents({})

    return templates.TemplateResponse("/pages/order/index.html", {
        "request": request,
        "title": "Order",
        "current_page": "order",
        "description": "Create, update the resource."
    })

# POST: Create new resource
@router.post("/create")
async def create_order (request: Request):
    
    form = await request.form()

    form_data = {
        "name": form.get("name")
    }

    result = await db_instance.db['order'].insert_one(form_data)

    return {
        "message": "Order created successfully!"
    }

