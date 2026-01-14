import click
@click.group()
@click.version_option()
def cli():
    pass

from .commands.create import create
from .commands.info import info
from .commands.createfiles import createfiles
cli.add_command(create)
cli.add_command(info)
cli.add_command(createfiles)
if __name__ == '__main__':
    cli()