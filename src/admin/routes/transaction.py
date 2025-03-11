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
    result = await db_instance.db['transaction'].find().skip(skip).limit(limit).to_list(limit)
    total = await db_instance.db['transaction'].count_documents({})

    return templates.TemplateResponse("/pages/transaction/index.html", {
        "request": request,
        "title": "Transaction",
        "current_page": "transaction",
        "description": "Create, update the resource."
    })

# POST: Create new resource
@router.post("/create")
async def create_transaction (request: Request):
    
    form = await request.form()

    form_data = {
        "name": form.get("name")
    }

    result = await db_instance.db['transaction'].insert_one(form_data)

    return {
        "message": "Transaction created successfully!"
    }

