# Copyright (c) 2025, Meshub
# Licensed under the MIT License

"""Justice commands for Meshub CLI."""

import click
import json
from meshub.commands.common import api_key_option, require_api_key, debug_option


@click.group()
def justice() -> None:
    """Justice data commands."""


@justice.command()
@api_key_option
@debug_option
def list_entities(api_key: str | None, debug: bool) -> None:
    """List available justice entities."""
    require_api_key(api_key, debug)
    # TODO: Implement actual API call
    entities: list[dict[str, str]] = []
    print(json.dumps(entities, indent=2))
