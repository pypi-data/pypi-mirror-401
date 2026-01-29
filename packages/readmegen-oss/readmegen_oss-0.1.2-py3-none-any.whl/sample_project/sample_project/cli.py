"""Command-line interface for sample-project."""

import click


@click.group()
@click.version_option(version="0.1.0")
def main():
    """Sample Python project CLI."""
    pass


@main.command()
@click.argument('name')
def greet(name):
    """Greet someone by name."""
    click.echo(f"Hello, {name}!")


@main.command()
def version():
    """Show version information."""
    click.echo("sample-project v0.1.0")


if __name__ == "__main__":
    main()
