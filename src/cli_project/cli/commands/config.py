import click
import json
import os

CONFIG_FILE = "config.json"

@click.command()
@click.option('--set', nargs=2, metavar='<key> <value>', help='Set a config value.')
@click.option('--get', metavar='<key>', help='Get a config value.')
def config(set, get):
    """Manage configuration."""

    # Create file if it doesn't exist
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as f:
            json.dump({}, f)

    # Try to read the config, handle if it's empty or broken
    try:
        with open(CONFIG_FILE, 'r') as f:
            content = f.read().strip()
            data = json.loads(content) if content else {}
    except json.JSONDecodeError:
        click.secho("⚠️  config.json is corrupted. Resetting to empty config.", fg="red")
        data = {}
        with open(CONFIG_FILE, 'w') as f:
            json.dump(data, f)

    # Set config value
    if set:
        key, value = set
        data[key] = value
        with open(CONFIG_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        click.secho(f"🔧 Set {key} = {value}", fg="cyan")

    # Get config value
    elif get:
        value = data.get(get, None)
        if value:
            click.secho(f"{get} = {value}", fg="yellow")
        else:
            click.secho(f"⚠️  Key '{get}' not found", fg="red")
    else:
        click.echo("Use --set <key> <value> or --get <key>")
