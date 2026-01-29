"""Topic abstract application module."""

# Due to typer usage:
# ruff: noqa: TC003

from __future__ import annotations

import logging
from collections.abc import Iterable
from typing import TYPE_CHECKING, Self

import typer

if TYPE_CHECKING:
    from . import description as desc
    from . import visitor

_LOGGER = logging.getLogger(__name__)


class Topic:
    """Topic application."""

    @classmethod
    def new(
        cls,
        topic_description: desc.Description,
        tools_type: type[visitor.Tools],
        tool_apps: Iterable[typer.Typer],
    ) -> Self:
        """Build topic application."""
        tool_apps = list(tool_apps)
        if len(tool_apps) != len(tools_type):
            _LOGGER.critical(
                "Number of tool applications (%d)"
                " differs from number of tools (%d) for topic `%s`",
                len(tool_apps),
                len(tools_type),
                topic_description.name(),
            )
            raise typer.Exit(1)
        app = typer.Typer(
            name=topic_description.cmd(),
            help=f"Subcommand for topic `{topic_description.name()}`",
            rich_markup_mode="rich",
        )
        for tool_app in tool_apps:
            app.add_typer(tool_app)
        return cls(tools_type, app)

    def __init__(self, tools: type[visitor.Tools], app: typer.Typer) -> None:
        self._tools = tools
        self._app = app

    def tools(self) -> type[visitor.Tools]:
        """Get tools."""
        return self._tools

    def app(self) -> typer.Typer:
        """Get app."""
        return self._app
