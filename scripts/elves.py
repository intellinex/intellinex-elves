#!/usr/bin/env python3
import click
from pathlib import Path

@click.group()
def cli():
    """Elves CLI for FastAPI project automation."""
    pass


# Generate Model
# using command: elves create-model [model-name]
@cli.command()
@click.argument("model_name")
def create_model(model_name):
    """
    Generate a FastAPI model file with the given model name.
    """
    # Define the target directory
    models_dir = Path("src/model")
    models_dir.mkdir(parents=True, exist_ok=True)  

    filename = models_dir / f"{model_name.lower()}_model.py"
    content = f"""\
from pydantic import BaseModel

class {model_name}(BaseModel):
    \"\"\"
    {model_name} model for FastAPI.
    \"\"\"
    id: int
    name: str
    description: str | None = None

# Example usage:
# {model_name.lower()} = {model_name}(id=1, name="Example", description="This is an example model.")
"""

    try:
        with open(filename, "w") as f:
            f.write(content)
        click.echo(f"Model file '{filename}' generated successfully.")
    except Exception as e:
        click.echo(f"Error: {e}")


# Generate Schema
# using command: elves create-model [model-name]
@cli.command()
@click.argument("model_name")
def schema(model_name):
    """
    Generate a FastAPI schema file with the given model name.
    """
    # Define the target directory
    models_dir = Path("src/schema")
    models_dir.mkdir(parents=True, exist_ok=True)  

    filename = models_dir / f"{model_name.lower()}_model.py"
    content = f"""\
from pydantic import BaseModel

class {model_name}(BaseModel):
    \"\"\"
    {model_name} model for FastAPI.
    \"\"\"
    id: int
    name: str
    description: str | None = None

# Example usage:
# {model_name.lower()} = {model_name}(id=1, name="Example", description="This is an example schema.")
"""

    try:
        with open(filename, "w") as f:
            f.write(content)
        click.echo(f"Schema file '{filename}' generated successfully.")
    except Exception as e:
        click.echo(f"Error: {e}")

##
# COMMAND FOR GENERATE ENDPOINT or CONTROLLER
# Usage: elves endpoint [enpoint-name]
# #

@cli.command()
@click.argument("endpoint_name")
def endpoint(endpoint_name):
    """
    Generate a FastAPI endpoint file with the given endpoint name.
    """
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



##
# COMMAND FOR GENERATE RESOURCE
# Usage: elves resource Location
# #

@cli.command()
@click.argument("endpoint_name")
def resource(endpoint_name):
    """
    Generate a FastAPI Resource file with the given endpoint name.
    """
    # Define the target directory
    endpoints_dir = Path("src/admin/routes")
    endpoints_dir.mkdir(parents=True, exist_ok=True)

    # Define the filename
    filename = endpoints_dir / f"{endpoint_name.lower()}.py"

    content = f"""\
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter()
templates = Jinja2Templates(directory="templates/pages")

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "{endpoint_name}",
        "current_page": "{endpoint_name.lower()}"
    })
"""
    
    # Write the content to the file
    try:
        with open(filename, "w") as f:
            f.write(content)
        click.echo(f"Resource file '{filename}' generated successfully.")
    except Exception as e:
        click.echo(f"Error: {e}")


if __name__ == "__main__":
    cli()