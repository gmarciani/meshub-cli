# Copyright (c) 2025, Meshub
# Licensed under the MIT License

"""Main CLI module for Meshub CLI."""

import click
import logging
from meshub.constants import __version__
from meshub.commands import config
from meshub.commands import justice
from meshub.commands import government
from meshub.commands import demography
from meshub.commands import firmography


@click.group()
@click.version_option(version=__version__, prog_name="meshub")
@click.option("--debug", "-d", is_flag=True, help="Enable debug output")
@click.pass_context
def main(ctx: click.Context, debug: bool) -> None:
    """Meshub CLI - Official CLI for Meshub."""
    ctx.ensure_object(dict)
    ctx.obj["debug"] = debug

    # Configure logging
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%SZ",
    )
    logging.Formatter.converter = lambda *args: __import__("time").gmtime()


# Add command groups
main.add_command(config.config)
main.add_command(justice.justice)
main.add_command(government.government)
main.add_command(demography.demography)
main.add_command(firmography.firmography)


if __name__ == "__main__":
    main()
