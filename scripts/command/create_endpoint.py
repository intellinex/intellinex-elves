from typing import List
import click
from pathlib import Path

def create_endpoint_command(endpoint_name):
    # Define the target directory
    endpoints_dir = Path("src/api/v1/endpoint")
    endpoints_dir.mkdir(parents=True, exist_ok=True)

    routes_dir = Path("src/api/v1")
    routes_dir.mkdir(parents=True, exist_ok=True)

    # Define the filename
    filename = endpoints_dir / f"{endpoint_name.lower()}.py"
    routes_file = routes_dir / "routes.py"

    # Define the content of the endpoint file
    content = f"""\
from fastapi import APIRouter, Depends, Form, Query, HTTPException
from src.model.{endpoint_name.lower()} import {endpoint_name.capitalize()}, {endpoint_name.capitalize()}Create, {endpoint_name.capitalize()}Update
from src.db.mongodb import get_async_db
from src.util.serial import serialize_document
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection
from bson import ObjectId

router = APIRouter()

# Dependency to get the database
async def get_{endpoint_name.lower()}_collection(db: AsyncIOMotorDatabase = Depends(get_async_db)):
    collection = db["{endpoint_name.lower()}"]
    await collection.create_index([("_id", 1)])  # Default _id index
    return collection


@router.post("/index")
async def get_{endpoint_name}s(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    collection: AsyncIOMotorCollection = Depends(get_{endpoint_name.lower()}_collection)
):
    \"\"\"Get paginated list of {endpoint_name}s.\"\"\"
    skip = (page - 1) * limit
    total = await collection.count_documents({{}})
    
    cursor = collection.find().sort("_id", -1).skip(skip).limit(limit)
    results = await cursor.to_list(length=limit)
    
    return {{
        "status": {{
            "code": 1,
            "message": "Success",
            "status": "success"
        }},
        "result": {{
            "data": [serialize_document(item) for item in results],
            "current_page": page,
            "total_pages": (total + limit - 1) // limit,
            "per_page": limit,
            "total_items": total
        }}
    }}


    
@router.post("/index/{{id}}")
async def get_{endpoint_name.lower()}_detail(
    id: str,
    collection: AsyncIOMotorCollection = Depends(get_{endpoint_name.lower()}_collection)
):
    \"\"\"Get a {endpoint_name} by ID.\"\"\"
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    # Check if the {endpoint_name} exists
    {endpoint_name.lower()}_id = ObjectId(id)
    {endpoint_name.lower()} = await collection.find_one({{"_id": {endpoint_name.lower()}_id}})
    if {endpoint_name.lower()} is None:
        raise HTTPException(status_code=404, detail="{endpoint_name.capitalize()} not found")
    return {{
        "status": {{
            "code": 1,
            "message": "Success",
            "status": "success"
        }},
        "result": {{
            "data": serialize_document({endpoint_name.lower()})
        }}
    }}
    

@router.post("/create")
async def create_career(
    form_data: {endpoint_name.capitalize()}Create,
    collection: AsyncIOMotorCollection = Depends(get_{endpoint_name.lower()}_collection),
):
    \"\"\"Create a new {endpoint_name}.\"\"\"
    {endpoint_name.lower()}_dict = form_data.dict()
    {endpoint_name.lower()}_dict["_id"] = ObjectId()
    result = await collection.insert_one({endpoint_name.lower()}_dict)
    if result.acknowledged:
        return {{
            "status": {{
                "code": 1,
                "message": "{endpoint_name.capitalize()} created successfully",
                "status": "success"
            }},
            "result": {{ 
                "data": serialize_document({endpoint_name.lower()}_dict) 
            }}
        }}
    else:
        raise HTTPException(status_code=500, detail="Failed to create {endpoint_name.capitalize()}")


@router.post("/update/{{id}}")
async def update_career(
    id: str,
    form_data: {endpoint_name.capitalize()}Update,
    collection: AsyncIOMotorCollection = Depends(get_{endpoint_name.lower()}_collection),
):
    \"\"\"Update a {endpoint_name}.\"\"\"
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    {endpoint_name.lower()}_id = ObjectId(id)

    # Check if the {endpoint_name} exists
    existing_{endpoint_name.lower()} = await collection.find_one({{"_id": {endpoint_name.lower()}_id}})
    if not existing_{endpoint_name.lower()}:
        raise HTTPException(status_code=404, detail="{endpoint_name.capitalize()} not found")

    # Proceed to update the {endpoint_name}
    {endpoint_name.lower()}_dict = form_data.dict(exclude_unset=True)
    result = await collection.update_one(
        {{"_id": {endpoint_name.lower()}_id}},
        {{"$set": {endpoint_name.lower()}_dict}},
    )
    if result.modified_count > 0:

        update_result = await collection.find_one({{"_id": {endpoint_name.lower()}_id}})    
    
        return {{
            "status": {{
                "code": 1,
                "message": "{endpoint_name.capitalize()} updated successfully",
                "status": "success",
            }},
            "result": {{
                "data": serialize_document(update_result)
            }}
        }}
    else:
        raise HTTPException(status_code=404, detail="{endpoint_name.capitalize()} not found")

        

@router.post("/delete/{{id}}")
async def delete_career(
    id: str,
    collection: AsyncIOMotorCollection = Depends(get_{endpoint_name.lower()}_collection),
):
    \"\"\"Delete a {endpoint_name}.\"\"\"
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    {endpoint_name.lower()}_id = ObjectId(id)

    # Check if the {endpoint_name} exists
    existing_{endpoint_name.lower()} = await collection.find_one({{"_id": {endpoint_name.lower()}_id}})
    if not existing_{endpoint_name.lower()}:
        raise HTTPException(status_code=404, detail="{endpoint_name.capitalize()} not found")

        
    # Proceed to delete the {endpoint_name}
    # Delete the {endpoint_name}
    result = await collection.delete_one({{"_id": ObjectId(id)}})
    if result.deleted_count > 0:
        return {{
            "status": {{
                "code": 1,
                "message": "{endpoint_name.capitalize()} deleted successfully",
                "status": "success",
            }},
            "result": {{"data": None}},
        }}
    else:
        raise HTTPException(status_code=404, detail="{endpoint_name.capitalize()} not found")

"""
    
    new_import = f"from src.api.v1.endpoint import {endpoint_name.lower()}"
    new_router = f"api_router.include_router({endpoint_name.lower()}.router, prefix=\"/{endpoint_name.lower()}\", tags=['{endpoint_name}'])"
    

    # Write the content to the file
    try:
        # Create endpoint file
        filename.write_text(content)
        click.echo(f"✅ Created endpoint: {filename}")

        # Update routes file
        if not routes_file.exists():
            routes_file.write_text("""\
from fastapi import APIRouter
api_router = APIRouter()
""")

        routes_content = routes_file.read_text().splitlines()
        updated_content = update_routes_content(routes_content, new_import, new_router)
        routes_file.write_text("\n".join(updated_content))
        
        click.echo(f"✅ Updated routes: {routes_file}")

    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)

def update_routes_content(existing_content: List[str], new_import: str, new_router: str) -> List[str]:
    """Update routes file content with new imports and routes."""
    imports = []
    router_def = []
    other_content = []
    current_section = imports
    
    for line in existing_content:
        if line.strip() == "api_router = APIRouter()":
            current_section = router_def
        elif line.strip().startswith("api_router.include_router("):
            current_section = other_content
        current_section.append(line)
    
    # Add new import if not exists
    if new_import not in imports:
        imports.insert(1, new_import)  # Insert after APIRouter import
    
    # Add new router if not exists
    if new_router not in router_def:
        router_def.append(new_router)
    
    return imports + [""] + router_def + ([""] + other_content if other_content else [])


@click.command()
@click.argument("endpoint_name")
def create_endpoint(endpoint_name):
    """
    Generate a FastAPI <<ENDPOINT>> file with the given endpoint name.

    """
    create_endpoint_command(endpoint_name)