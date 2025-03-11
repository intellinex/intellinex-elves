import click
from pathlib import Path

def create_model_command(model_name):
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
        click.echo(f"✅ 🚀 Model file '{filename}' generated successfully.\n")
    except Exception as e:
        click.echo(f"❌ Error: {e}\n")


@click.command()
@click.argument("model_name")
def create_model(model_name):
    """
    Generate a FastAPI <<MODEL>> file with the given model name.
    """
    create_model_command(model_name)