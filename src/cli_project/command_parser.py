import click
from cli.commands.init import init
from cli.commands.config import config
from cli.commands.build import build

@click.group()
@click.version_option("1.0.0", prog_name="MyCLI")
def cli():
    """🔧 MyCLI - A Project Command Line Tool."""
    pass

cli.add_command(init)
cli.add_command(config)
cli.add_command(build)

if __name__ == '__main__':
    cli()
