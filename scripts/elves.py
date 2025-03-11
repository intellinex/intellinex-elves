#!/usr/bin/env python3
import click
from scripts.command import (
    create_dropdown,
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
cli.add_command(create_dropdown.create_dropdown, "create-dropdown")


if __name__ == "__main__":
    cli()