import click

@click.command()
@click.option('--env', default='dev', type=click.Choice(['dev', 'prod'], case_sensitive=False))
def build(env):
    """Build the project for deployment."""
    click.secho(f"🚀 Building project for {env} environment...", fg="blue")
    # Simulate build steps...
    click.secho("✅ Build complete!", fg="green")
