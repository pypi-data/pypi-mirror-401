"""plmbench Platon application module."""

# Due to typer usage:

from __future__ import annotations

from slurmbench.prelude.tool import app as core

from . import connector, description

APP = core.new(description.DESCRIPTION, connector.Connector)
