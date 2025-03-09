from fastapi import APIRouter, HTTPException
from src.model.product_model import Product

router = APIRouter()

# Example in-memory database
product_db = []

@router.post("/product/", response_model=Product)
def create_product(item: Product):
    product_db.append(item)
    return item

@router.get("/product/", response_model=list[Product])
def read_product():
    return product_db

@router.get("/product/{item_id}", response_model=Product)
def read_product_by_id(item_id: int):
    if item_id < 0 or item_id >= len(product_db):
        raise HTTPException(status_code=404, detail="Item not found")
    return product_db[item_id]

@router.put("/product/{item_id}", response_model=Product)
def update_product_by_id(item_id: int, item: Product):
    if item_id < 0 or item_id >= len(product_db):
        raise HTTPException(status_code=404, detail="Item not found")
    product_db[item_id] = item
    return item

@router.delete("/product/{item_id}")
def delete_product_by_id(item_id: int):
    if item_id < 0 or item_id >= len(product_db):
        raise HTTPException(status_code=404, detail="Item not found")
    product_db.pop(item_id)
    return {"message": "Item deleted"}
