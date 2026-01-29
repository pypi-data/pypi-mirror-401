"""Metadata-related commands."""

from typing import Annotated

import typer

from nesso_cli.models.common import call_shell, wrapper_context_settings


app = typer.Typer()


@app.command(context_settings=wrapper_context_settings)
def generate(
    ctx: typer.Context,
    select: Annotated[
        str | None, typer.Option("--select", "-s", help="The model(s) to select.")
    ] = None,
) -> None:
    """Generate metadata for the project."""
    args = []
    if select:
        args.extend(["-s", select])
    if ctx.args:
        args.extend(ctx.args)

    call_shell("dbt docs generate", args=args, print_logs=True)
