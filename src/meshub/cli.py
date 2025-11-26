# Copyright (c) 2025, Meshub
# Licensed under the MIT License

"""Main CLI module for Meshub CLI."""

import click
import logging
from meshub.constants import __version__
from meshub.commands import config


@click.group()
@click.version_option(version=__version__, prog_name="meshub")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.pass_context
def main(ctx: click.Context, verbose: bool) -> None:
    """Meshub CLI - Official CLI for Meshub."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose

    # Configure logging
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")


# Add command groups
main.add_command(config.config)


if __name__ == "__main__":
    main()
