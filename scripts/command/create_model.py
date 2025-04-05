import click
from pathlib import Path

def create_model_command(model_name):
    # Define the target directory
    models_dir = Path("src/model")
    models_dir.mkdir(parents=True, exist_ok=True)  

    filename = models_dir / f"{model_name.lower()}.py"
    content = f"""\
from pydantic import BaseModel
from datetime import datetime
from bson import ObjectId
from typing import Optional, List

class {model_name}(BaseModel):
    id: str
    title: str
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

class {model_name}Create(BaseModel):
    title: str
    created_at: datetime = datetime.utcnow()


class {model_name}Update(BaseModel):
    title: Optional[str] = None
    updated_at: datetime = datetime.utcnow()


class {model_name}InDB({model_name}):
    id: str
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
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