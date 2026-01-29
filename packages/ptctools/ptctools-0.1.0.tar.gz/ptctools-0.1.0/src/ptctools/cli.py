"""Main CLI entry point for ptctools."""

import click

from ptctools import __version__
from ptctools import stack
from ptctools import volume
from ptctools import db
from ptctools import utils
from ptctools import config


@click.group()
@click.version_option(version=__version__)
def main():
    """Portainer Client Tools - manage stacks, volumes, and databases."""
    pass


main.add_command(stack.cli, name="stack")
main.add_command(volume.cli, name="volume")
main.add_command(db.cli, name="db")
main.add_command(utils.cli, name="utils")
main.add_command(config.cli, name="config")


if __name__ == "__main__":
    main()
