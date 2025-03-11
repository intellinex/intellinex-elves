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
@click.option("--group", default=None, help="Add the resource to an existing group in the sidebar.")
def resource(endpoint_name, group):
    """
    Generate a FastAPI Resource with Group Sidebar file with the given resource name and update the router and sidebar.
    If a group is specified, add the resource to the existing group's menu file.
    """
    # Define the target directories
    endpoints_dir = Path("src/admin/routes")
    endpoints_dir.mkdir(parents=True, exist_ok=True)
    admin_dir = Path("src/admin")
    templates_dir = Path(f"templates/pages/{endpoint_name.lower()}")
    templates_dir.mkdir(parents=True, exist_ok=True)

    # Define the filename for the new resource
    filename = endpoints_dir / f"{endpoint_name.lower()}.py"
    template_file = templates_dir / "index.html"

    # Define menu directory and file
    if group:
        menu_dir = Path(f"static/components/{group.lower()}")
        menu_file = menu_dir / "menu.html"
    else:
        menu_dir = Path(f"static/components/{endpoint_name.lower()}")
        menu_file = menu_dir / "menu.html"
    menu_dir.mkdir(parents=True, exist_ok=True)

    # Define the content of the resource file
    content = f"""\
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
    result = await db_instance.db['{endpoint_name.lower()}'].find().skip(skip).limit(limit).to_list(limit)
    total = await db_instance.db['{endpoint_name.lower()}'].count_documents({{}})

    return templates.TemplateResponse("/pages/{endpoint_name.lower()}/index.html", {{
        "request": request,
        "title": "{endpoint_name}",
        "current_page": "{endpoint_name.lower()}",
        "description": "Create, update the resource."
    }})

# POST: Create new resource
@router.post("/create")
async def create_{endpoint_name.lower()} (request: Request):
    
    form = await request.form()

    form_data = {{
        "name": form.get("name")
    }}

    result = await db_instance.db['{endpoint_name.lower()}'].insert_one(form_data)

    return {{
        "message": "{endpoint_name} created successfully!"
    }}

"""

    # Template content
    templates = f"""\
{{% extends "layout.html" %}}
{{% block title %}} {endpoint_name} {{% endblock %}}

{{% block content %}}
<!-- Custom your content -->
{{% endblock %}}
"""

    # Menu content

    menu_content = f"""\
<li>
    <a href="/{endpoint_name.lower()}" class="d-flex flex-row align-items-center justify-content-between {{current_page}} "aria-current="page">
        <div class="d-flex align-items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-gallery-vertical-end"><path d="M7 2h10"/><path d="M5 6h14"/><rect width="18" height="12" x="3" y="10" rx="2"/></svg>
            <span>{endpoint_name}</span>
        </div>
    </a>
</li>
"""
    # Write the content to the new resource file
    try:
        with open(filename, "w") as f:
            f.write(content)
        click.echo(f"Resource file '{filename}' generated successfully.")
        with open(template_file, "w") as t:
            t.write(templates)
        click.echo(f"Template file '{template_file}' created successfully.")
    except Exception as e:
        click.echo(f"Error: {e}")
        return

    # Update the router file
    router_file = admin_dir / "routers.py"
    try:
        with open(router_file, "r") as f:
            lines = f.readlines()

        # Find the line where imports end and the router definition starts
        import_end_index = next(
            (i for i, line in enumerate(lines) if line.strip().startswith("app_router = APIRouter()")),
            len(lines),
        )

        # Add the new import
        new_import = f"from src.admin.routes import {endpoint_name.lower()}\n"
        if new_import not in lines:
            lines.insert(import_end_index - 1, new_import)

        # Add the new include_router statement
        new_include = f'app_router.include_router(router={endpoint_name.lower()}.router, prefix="/{endpoint_name.lower()}")\n'
        if new_include not in lines:
            lines.append(new_include)

        # Write the updated content back to the file
        with open(router_file, "w") as f:
            f.writelines(lines)
        click.echo(f"Router file '{router_file}' updated successfully.")
    except Exception as e:
        click.echo(f"Error updating router file: {e}")

    # Update the menu file
    try:
        if group:
            # If a group is specified, append the new <li> to the existing menu file
            if menu_file.exists():
                with open(menu_file, "a") as f:
                    f.write(menu_content)
                click.echo(f"Menu file '{menu_file}' updated successfully.")
            else:
                with open(menu_file, "w") as f:
                    f.write(menu_content)
                click.echo(f"Menu file '{menu_file}' created successfully.")
        else:
            # If no group is specified, create a new menu file
            with open(menu_file, "w") as f:
                f.write(menu_content)
            click.echo(f"Menu file '{menu_file}' created successfully.")
    except Exception as e:
        click.echo(f"Error updating menu file: {e}")

    # Update the sidebar file (static/js/main.js)
    try:
        with open("static/js/main.js", "r") as f:
            sidebar_content = f.read()

        if group:
            # Add the new loadNavItem call for the existing group
            new_load_nav_item = f"""
            await this.loadNavItem('/static/components/{group.lower()}/menu.html', '{group.lower()}-nav', current_page);
            """

            # Find the position to insert the new loadNavItem call
            load_nav_insert_position = sidebar_content.find('this.addEventListeners();')
            if load_nav_insert_position == -1:
                raise ValueError("Could not find 'this.addEventListeners();' in sidebar file.")

            # Insert the new loadNavItem call
            updated_sidebar_content = (
                sidebar_content[:load_nav_insert_position] +
                new_load_nav_item +
                sidebar_content[load_nav_insert_position:]
            )
        else:
            # If no group is specified, create a new group (same as before)
            new_nav = f"""
            <!-- GROUP {endpoint_name} -->
            <nav>
                <span class="c_label">{endpoint_name}</span>
                <ul class="c_nav" id="{endpoint_name.lower()}-nav"></ul>
            </nav>
            """

            # Find the position to insert the new <nav> section
            nav_insert_position = sidebar_content.find('<!-- Customize Layout -->')
            if nav_insert_position == -1:
                raise ValueError("Could not find '<!-- Customize Layout -->' in sidebar file.")

            # Insert the new <nav> section
            updated_sidebar_content = (
                sidebar_content[:nav_insert_position] +
                new_nav +
                sidebar_content[nav_insert_position:]
            )

            # Add the new loadNavItem call
            new_load_nav_item = f"""
            await this.loadNavItem('/static/components/{endpoint_name.lower()}/menu.html', '{endpoint_name.lower()}-nav', current_page);
            """

            # Find the position to insert the new loadNavItem call
            load_nav_insert_position = updated_sidebar_content.find('this.addEventListeners();')
            if load_nav_insert_position == -1:
                raise ValueError("Could not find 'this.addEventListeners();' in sidebar file.")

            # Insert the new loadNavItem call
            updated_sidebar_content = (
                updated_sidebar_content[:load_nav_insert_position] +
                new_load_nav_item +
                updated_sidebar_content[load_nav_insert_position:]
            )

        # Write the updated content back to the file
        with open("static/js/main.js", "w") as f:
            f.write(updated_sidebar_content)
        click.echo("Sidebar file 'static/js/main.js' updated successfully.")
    except Exception as e:
        click.echo(f"Error updating sidebar file: {e}")



@cli.command()
@click.argument("endpoint_name")
@click.option("--group", default=None, help="Add the resource to an existing group in the sidebar.")
def resource_dropdown(endpoint_name, group):
    """
    Generate a FastAPI Resource with Group Sidebar file with the given resource name and update the router and sidebar.
    If a group is specified, add the resource to the existing group's menu file.
    """
    # Define the target directories
    endpoints_dir = Path("src/admin/routes")
    endpoints_dir.mkdir(parents=True, exist_ok=True)
    admin_dir = Path("src/admin")
    templates_dir = Path(f"templates/pages/{endpoint_name.lower()}")
    templates_dir.mkdir(parents=True, exist_ok=True)

    # Define the filename for the new resource
    filename = endpoints_dir / f"{endpoint_name.lower()}.py"
    template_file = templates_dir / "index.html"

    # Define menu directory and file
    if group:
        menu_dir = Path(f"static/components/{group.lower()}")
        menu_file = menu_dir / "menu.html"
    else:
        menu_dir = Path(f"static/components/{endpoint_name.lower()}")
        menu_file = menu_dir / "menu.html"
    menu_dir.mkdir(parents=True, exist_ok=True)

    # Define the content of the resource file
    content = f"""\
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
    result = await db_instance.db['{endpoint_name.lower()}'].find().skip(skip).limit(limit).to_list(limit)
    total = await db_instance.db['{endpoint_name.lower()}'].count_documents({{}})

    return templates.TemplateResponse("/pages/{endpoint_name.lower()}/index.html", {{
        "request": request,
        "title": "{endpoint_name}",
        "current_page": "{endpoint_name.lower()}",
        "description": "Create, update the resource."
    }})

# POST: Create new resource
@router.post("/create")
async def create_{endpoint_name.lower()} (request: Request):
    
    form = await request.form()

    form_data = {{
        "name": form.get("name")
    }}

    result = await db_instance.db['{endpoint_name.lower()}'].insert_one(form_data)

    return {{
        "message": "{endpoint_name} created successfully!"
    }}

"""

    # Template content
    templates = f"""\
{{% extends "layout.html" %}}
{{% block title %}} {endpoint_name} {{% endblock %}}

{{% block content %}}
<!-- Custom your content -->
{{% endblock %}}
"""

    # Menu content
    
    menu_content = f"""\
<li>
    <a href="#" id="{endpoint_name.lower()}" class="d-flex flex-row align-items-center justify-content-between {{current_page}}"
    aria-current="page">
        <div class="d-flex align-items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-gallery-vertical-end"><path d="M7 2h10"/><path d="M5 6h14"/><rect width="18" height="12" x="3" y="10" rx="2"/></svg>
            <span>{endpoint_name}</span>
        </div>
        <div class="dropdown-arrow" id="dropdown-arrow-{endpoint_name.lower()}">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24"
                fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                stroke-linejoin="round" class="lucide lucide-chevron-right">
                <path d="m9 18 6-6-6-6"/>
            </svg>
        </div>
    </a>

    <!-- Dropdown Menu -->
    <ul class="c_dropdown_menu" id"c_dropdown_menu_{endpoint_name.lower()}">
        <li><a href="/user" class="d-flex align-items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-gallery-vertical-end"><path d="M7 2h10"/><path d="M5 6h14"/><rect width="18" height="12" x="3" y="10" rx="2"/></svg>
            <span>Item 1</span>
        </a></li>
        <li><a href="#" class="d-flex align-items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-gallery-vertical-end"><path d="M7 2h10"/><path d="M5 6h14"/><rect width="18" height="12" x="3" y="10" rx="2"/></svg>
            <span>Item 2</span>
        </a></li>
        <li><a href="#" class="d-flex align-items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-gallery-vertical-end"><path d="M7 2h10"/><path d="M5 6h14"/><rect width="18" height="12" x="3" y="10" rx="2"/></svg>
            <span>Item 3</span>
        </a></li>
    </ul>
</li>
"""

    # Write the content to the new resource file
    try:
        with open(filename, "w") as f:
            f.write(content)
        click.echo(f"Resource file '{filename}' generated successfully.")
        with open(template_file, "w") as t:
            t.write(templates)
        click.echo(f"Template file '{template_file}' created successfully.")
    except Exception as e:
        click.echo(f"Error: {e}")
        return

    # Update the router file
    router_file = admin_dir / "routers.py"
    try:
        with open(router_file, "r") as f:
            lines = f.readlines()

        # Find the line where imports end and the router definition starts
        import_end_index = next(
            (i for i, line in enumerate(lines) if line.strip().startswith("app_router = APIRouter()")),
            len(lines),
        )

        # Add the new import
        new_import = f"from src.admin.routes import {endpoint_name.lower()}\n"
        if new_import not in lines:
            lines.insert(import_end_index - 1, new_import)

        # Add the new include_router statement
        new_include = f'app_router.include_router(router={endpoint_name.lower()}.router, prefix="/{endpoint_name.lower()}")\n'
        if new_include not in lines:
            lines.append(new_include)

        # Write the updated content back to the file
        with open(router_file, "w") as f:
            f.writelines(lines)
        click.echo(f"Router file '{router_file}' updated successfully.")
    except Exception as e:
        click.echo(f"Error updating router file: {e}")

    # Update the menu file
    try:
        if group:
            # If a group is specified, append the new <li> to the existing menu file
            if menu_file.exists():
                with open(menu_file, "a") as f:
                    f.write(menu_content)
                click.echo(f"Menu file '{menu_file}' updated successfully.")
            else:
                with open(menu_file, "w") as f:
                    f.write(menu_content)
                click.echo(f"Menu file '{menu_file}' created successfully.")
        else:
            # If no group is specified, create a new menu file
            with open(menu_file, "w") as f:
                f.write(menu_content)
            click.echo(f"Menu file '{menu_file}' created successfully.")
    except Exception as e:
        click.echo(f"Error updating menu file: {e}")

    # Update the sidebar file (static/js/main.js)
    try:
        with open("static/js/main.js", "r") as f:
            sidebar_content = f.read()

        if group:
            # Add the new loadNavItem call for the existing group
            new_load_nav_item = f"""
            await this.loadNavItem('/static/components/{group.lower()}/menu.html', '{group.lower()}-nav', current_page);
            """

            # Find the position to insert the new loadNavItem call
            load_nav_insert_position = sidebar_content.find('this.addEventListeners();')
            if load_nav_insert_position == -1:
                raise ValueError("Could not find 'this.addEventListeners();' in sidebar file.")

            # Insert the new loadNavItem call
            updated_sidebar_content = (
                sidebar_content[:load_nav_insert_position] +
                new_load_nav_item +
                sidebar_content[load_nav_insert_position:]
            )
        else:
            # If no group is specified, create a new group (same as before)
            new_nav = f"""
            <!-- GROUP {endpoint_name} -->
            <nav>
                <span class="c_label">{endpoint_name}</span>
                <ul class="c_nav" id="{endpoint_name.lower()}-nav"></ul>
            </nav>
            """

            # Find the position to insert the new <nav> section
            nav_insert_position = sidebar_content.find('<!-- Customize Layout -->')
            if nav_insert_position == -1:
                raise ValueError("Could not find '<!-- Customize Layout -->' in sidebar file.")

            # Insert the new <nav> section
            updated_sidebar_content = (
                sidebar_content[:nav_insert_position] +
                new_nav +
                sidebar_content[nav_insert_position:]
            )

            # Add the new loadNavItem call
            new_load_nav_item = f"""
            await this.loadNavItem('/static/components/{endpoint_name.lower()}/menu.html', '{endpoint_name.lower()}-nav', current_page);
            """

            # Find the position to insert the new loadNavItem call
            load_nav_insert_position = updated_sidebar_content.find('this.addEventListeners();')
            if load_nav_insert_position == -1:
                raise ValueError("Could not find 'this.addEventListeners();' in sidebar file.")

            # Insert the new loadNavItem call
            updated_sidebar_content = (
                updated_sidebar_content[:load_nav_insert_position] +
                new_load_nav_item +
                updated_sidebar_content[load_nav_insert_position:]
            )

        # Write the updated content back to the file
        with open("static/js/main.js", "w") as f:
            f.write(updated_sidebar_content)
        click.echo("Sidebar file 'static/js/main.js' updated successfully.")
    except Exception as e:
        click.echo(f"Error updating sidebar file: {e}")


if __name__ == "__main__":
    cli()