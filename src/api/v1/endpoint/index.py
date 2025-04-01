from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def index():
    return {
        "code": 1,
        "message": "You have successfully setup ELVES-API.",
        "status": "success",
        "data": 1
    }

@router.post("/token")
async def api_key():
    return {
        "API_KEY": "doifhry5487ty4857ty58t47g7"
    }