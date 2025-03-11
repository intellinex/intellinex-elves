import click
from pathlib import Path

def create_resource_command(resource_name, group):
    # Define the target directories
    endpoints_dir = Path("src/admin/routes")
    endpoints_dir.mkdir(parents=True, exist_ok=True)
    admin_dir = Path("src/admin")
    templates_dir = Path(f"templates/pages/{resource_name.lower()}")
    templates_dir.mkdir(parents=True, exist_ok=True)

    # Define the filename for the new resource
    filename = endpoints_dir / f"{resource_name.lower()}.py"
    template_file = templates_dir / "index.html"

    # Define menu directory and file
    # If add to group , we don't need to create new menu.html
    if group:
        menu_dir = Path(f"static/components/{group.lower()}")
        menu_file = menu_dir / "menu.html"
    else:
        menu_dir = Path(f"static/components/{resource_name.lower()}")
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
    result = await db_instance.db['{resource_name.lower()}'].find().skip(skip).limit(limit).to_list(limit)
    total = await db_instance.db['{resource_name.lower()}'].count_documents({{}})

    return templates.TemplateResponse("/pages/{resource_name.lower()}/index.html", {{
        "request": request,
        "title": "{resource_name}",
        "current_page": "{resource_name.lower()}",
        "description": "Create, update the resource."
    }})

# POST: Create new resource
@router.post("/create")
async def create_{resource_name.lower()} (request: Request):
    
    form = await request.form()

    form_data = {{
        "name": form.get("name")
    }}

    result = await db_instance.db['{resource_name.lower()}'].insert_one(form_data)

    return {{
        "message": "{resource_name} created successfully!"
    }}

"""

    # Template content
    templates = f"""\
{{% extends "layout.html" %}}
{{% block title %}} {resource_name} {{% endblock %}}

{{% block content %}}
<!-- Custom your content -->
{{% endblock %}}
"""

    # Menu content

    menu_content = f"""\
<li>
    <a href="/{resource_name.lower()}" class="d-flex flex-row align-items-center justify-content-between {{current_page}} "aria-current="page">
        <div class="d-flex align-items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-gallery-vertical-end"><path d="M7 2h10"/><path d="M5 6h14"/><rect width="18" height="12" x="3" y="10" rx="2"/></svg>
            <span>{resource_name}</span>
        </div>
    </a>
</li>
"""
    # Write the content to the new resource file
    try:
        with open(filename, "w") as f:
            f.write(content)
        click.echo(f"✅ Resource file '{filename}' generated successfully.\n")
        with open(template_file, "w") as t:
            t.write(templates)
        click.echo(f"✅ Template file '{template_file}' created successfully.\n")
    except Exception as e:
        click.echo(f"❌ Error: {e}\n")
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
        new_import = f"from src.admin.routes import {resource_name.lower()}\n"
        if new_import not in lines:
            lines.insert(import_end_index - 1, new_import)

        # Add the new include_router statement
        new_include = f'app_router.include_router(router={resource_name.lower()}.router, prefix="/{resource_name.lower()}")\n'
        if new_include not in lines:
            lines.append(new_include)

        # Write the updated content back to the file
        with open(router_file, "w") as f:
            f.writelines(lines)
        click.echo(f"✅ Router file '{router_file}' updated successfully.\n")
    except Exception as e:
        click.echo(f"❌ Error updating router file: {e}\n")

    # Update the menu file
    try:
        if group:
            # If a group is specified, append the new <li> to the existing menu file
            if menu_file.exists():
                with open(menu_file, "a") as f:
                    f.write(menu_content)
                click.echo(f"✅ Menu file '{menu_file}' updated successfully.\n")
            else:
                with open(menu_file, "w") as f:
                    f.write(menu_content)
                click.echo(f"✅ Menu file '{menu_file}' created successfully.\n")
        else:
            # If no group is specified, create a new menu file
            with open(menu_file, "w") as f:
                f.write(menu_content)
            click.echo(f"✅ Menu file '{menu_file}' created successfully.\n")
    except Exception as e:
        click.echo(f"Error updating menu file: {e}")



    # Update the sidebar file (static/js/main.js)
    # 
    #
    try:
        with open("static/js/main.js", "r") as f:
            sidebar_content = f.read()


        if not group:
            # If no group is specified, create a new group (same as before)
            new_nav = f"""
                    <!-- GROUP {resource_name} -->
                    <nav>
                        <span class="c_label">{resource_name}</span>
                        <ul class="c_nav" id="{resource_name.lower()}-nav"></ul>
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
        await this.loadNavItem('/static/components/{resource_name.lower()}/menu.html', '{resource_name.lower()}-nav');
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
            click.echo("✅ Sidebar file 'static/js/main.js' updated successfully.\n")

        print(f"🎨 Adding new resource to {group}.")
    except Exception as e:
        click.echo(f"❌ Error updating sidebar file: {e}\n")

@click.command()
@click.argument("resource_name")
@click.option("--group", default=None, help="Add the resource to an existing group in the sidebar.")
def create_resource(resource_name, group):
    """
    Generate a FastAPI Resource with Group Sidebar file with the given resource name and update the router and sidebar.
    If a group is specified, add the resource to the existing group's menu file.
    """
    create_resource_command(resource_name, group)