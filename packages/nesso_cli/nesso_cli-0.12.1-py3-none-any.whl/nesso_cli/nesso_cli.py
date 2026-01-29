"""Nesso CLI main module."""

from importlib.metadata import version
from pathlib import Path
from typing import Annotated

import typer

from nesso_cli import jobs, models


app = typer.Typer(rich_markup_mode="rich")
app.add_typer(models.main.app, name="models", short_help="Manage data models.")
app.add_typer(jobs.main.app, name="jobs", short_help="Manage ELT jobs.")


def cli() -> None:
    """For python script installation purposes."""
    app()


def version_callback(value: bool) -> None:
    """Print version number."""
    if value:
        cli_name = Path(__file__).stem
        print(f"{cli_name} {version(cli_name)}")  # noqa: T201
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[  # noqa: ARG001
        bool | None,
        typer.Option("--version", "-v", callback=version_callback, is_eager=True),
    ] = None,
) -> None:
    """Nesso CLI: Manage your data models and ELT jobs with ease."""
    return


if __name__ == "__main__":
    app()
