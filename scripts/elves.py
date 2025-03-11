#!/usr/bin/env python3
import click
from pathlib import Path
from scripts.command import (
    create_endpoint,
    create_model,
    create_resource,
    create_schema
)

@click.group()
def cli():
    """Elves CLI for FastAPI project automation."""
    pass

cli.add_command(create_model.create_model, "create-model")
cli.add_command(create_schema.create_schema, "create-schema")
cli.add_command(create_endpoint.create_endpoint, "create-endpoint")
cli.add_command(create_resource.create_resource, "create-resource")


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
    # This CONTENT will insert to src/admin/route/{endpoint_name}
    # For: Listing, Creating
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
    #
    #
    templates = f"""\
{{% extends "layout.html" %}}
{{% block title %}} {endpoint_name} {{% endblock %}}

{{% block content %}}
<!-- Custom your content -->
{{% endblock %}}
"""

    # Menu content
    # 
    #
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
            await this.loadNavItem('/static/components/{group.lower()}/menu.html', '{group.lower()}-nav');
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
            await this.loadNavItem('/static/components/{endpoint_name.lower()}/menu.html', '{endpoint_name.lower()}-nav');
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