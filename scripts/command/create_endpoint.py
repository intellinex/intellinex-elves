import click
from pathlib import Path

def create_endpoint_command(endpoint_name):
    # Define the target directory
    endpoints_dir = Path("src/api/v1/endpoint")
    endpoints_dir.mkdir(parents=True, exist_ok=True)

    # Define the filename
    filename = endpoints_dir / f"{endpoint_name.lower()}.py"

    # Define the content of the endpoint file
    content = f"""\
from fastapi import APIRouter, HTTPException
from src.model.{endpoint_name.lower()}_model import {endpoint_name}

router = APIRouter()

# Example in-memory database
{endpoint_name.lower()}_db = []

@router.post("/{endpoint_name.lower()}/", response_model={endpoint_name})
def create_{endpoint_name.lower()}(item: {endpoint_name}):
    {endpoint_name.lower()}_db.append(item)
    return item

@router.get("/{endpoint_name.lower()}/", response_model=list[{endpoint_name}])
def read_{endpoint_name.lower()}():
    return {endpoint_name.lower()}_db

@router.get("/{endpoint_name.lower()}/{{item_id}}", response_model={endpoint_name})
def read_{endpoint_name.lower()}_by_id(item_id: int):
    if item_id < 0 or item_id >= len({endpoint_name.lower()}_db):
        raise HTTPException(status_code=404, detail="Item not found")
    return {endpoint_name.lower()}_db[item_id]

@router.put("/{endpoint_name.lower()}/{{item_id}}", response_model={endpoint_name})
def update_{endpoint_name.lower()}_by_id(item_id: int, item: {endpoint_name}):
    if item_id < 0 or item_id >= len({endpoint_name.lower()}_db):
        raise HTTPException(status_code=404, detail="Item not found")
    {endpoint_name.lower()}_db[item_id] = item
    return item

@router.delete("/{endpoint_name.lower()}/{{item_id}}")
def delete_{endpoint_name.lower()}_by_id(item_id: int):
    if item_id < 0 or item_id >= len({endpoint_name.lower()}_db):
        raise HTTPException(status_code=404, detail="Item not found")
    {endpoint_name.lower()}_db.pop(item_id)
    return {{"message": "Item deleted"}}
"""

    # Write the content to the file
    try:
        with open(filename, "w") as f:
            f.write(content)
        click.echo(f"Endpoint file '{filename}' generated successfully.")
    except Exception as e:
        click.echo(f"Error: {e}")


@click.command()
@click.argument("endpoint_name")
def create_endpoint(endpoint_name):
    """
    Generate a FastAPI <<ENDPOINT>> file with the given endpoint name.
    """
    create_endpoint_command(endpoint_name)