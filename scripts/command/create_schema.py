import click
from pathlib import Path

def schema(schema_name):
    # Define the target directory
    models_dir = Path("src/schema")
    models_dir.mkdir(parents=True, exist_ok=True)  

    filename = models_dir / f"{schema_name.lower()}_schema.py"
    content = f"""\
from pydantic import BaseModel

class {schema_name}(BaseModel):
    \"\"\"
    {schema_name} model for FastAPI.
    \"\"\"
    id: int
    name: str
    description: str | None = None

# Example usage:
# {schema_name.lower()} = {schema_name}(id=1, name="Example", description="This is an example schema.")
"""

    try:
        with open(filename, "w") as f:
            f.write(content)
        click.echo(f"✅ 🚀 Schema file '{filename}' generated successfully.\n")
    except Exception as e:
        click.echo(f"❌ Error: {e}\n")

@click.command()
@click.argument("schema_name")
def create_schema(schema_name):
    """
    Generate a FastAPI <<SCHEMA>> file with the given model name.
    """
    schema(schema_name)