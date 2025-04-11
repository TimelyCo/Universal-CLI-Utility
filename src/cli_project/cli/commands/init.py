import click

@click.command()
def init():
    """Initialize the project."""
    # You can add project scaffolding here
    click.secho("✅ Project initialized successfully!", fg="green")
