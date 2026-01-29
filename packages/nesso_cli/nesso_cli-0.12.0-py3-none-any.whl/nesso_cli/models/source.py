"""Commands for managing source schemas and tables."""

from pathlib import Path
from textwrap import indent
from typing import Annotated

from rich import print as rprint
from rich.panel import Panel
from rich.prompt import Prompt
import typer

from nesso_cli.models import context
from nesso_cli.models.base_model import rm as base_model_rm
from nesso_cli.models.common import (
    check_if_relation_exists,
    get_current_dbt_project_obj,
    options,
    run_dbt_operation,
    wrapper_context_settings,
)
from nesso_cli.models.config import config, yaml


app = typer.Typer()


class SourceTableExistsError(Exception):
    pass


def _get_default_schema_path(source: str) -> Path:
    dbt_project_dir = Path(context.get("PROJECT_DIR"))
    schema_file_name = source + ".yml"
    return dbt_project_dir / "models" / "sources" / source / schema_file_name


def check_if_source_exists(source: str, schema_path: str | Path | None = None) -> bool:
    """Check if a source schema file exists and is valid.

    Args:
        source (str): The name of the source.
        schema_path (str | Path, optional): The path to the source schema file. Defaults
            to None.

    Returns:
        bool: True if the source schema file exists, False otherwise.

    """
    if schema_path is None:
        schema_path = _get_default_schema_path(source)

    # Enforce `pathlib.Path` type.
    schema_path = Path(schema_path)
    return schema_path.exists()


def check_if_source_table_exists(
    source: str, table_name: str, schema_path: str | Path | None = None
) -> bool:
    """Check if a source table exists in the source schema YAML.

    Args:
        source (str): The name of the source.
        table_name (str): The name of the table to check.
        schema_path (str | Path, optional): The path to the source schema file.
            Defaults to None.

    Returns:
        bool: True if the source table exists in the schema, False otherwise.

    """
    if schema_path is None:
        schema_path = _get_default_schema_path(source)

    if check_if_source_exists(source, schema_path=schema_path):
        representations = [
            f"- name: {table_name}\n",
            f'- name: "{table_name}"\n',
            f"- name: '{table_name}'\n",
        ]

        with Path(schema_path).open() as f:
            for line in f:
                for representation in representations:
                    if representation in line:
                        return True
    return False


def _create_table_docs(
    base_dir: Path,
    schema: str,
    table: str,
    profile: bool,
    target: str | None = None,
    non_interactive: bool | None = False,
) -> None:
    """Create documentation for a database table.

    Args:
        base_dir (Path): The base directory for storing the documentation.
        schema (str): The schema of the database table.
        table (str): The name of the database table.
        profile (bool): If True, profiles the source table. If False, creates a
            description template for the table.
        target (Optional[str], optional): The name of the dbt target to use.
            Defaults to None.
        non_interactive (Optional[str], optional): Whether to execute the function
            without interactive prompts. Defaults to False.

    """
    docs_path = base_dir.joinpath("docs", f"{table}.md")
    docs_path_trimmed = docs_path.relative_to(
        docs_path.parent.parent.parent.parent.parent
    )
    docs_path_fmt = f"[bright_black]{docs_path_trimmed}[/bright_black]"
    fqn_fmt = f"[white]{schema}.{table}[/white]"

    docs_path.parent.mkdir(exist_ok=True, parents=True)

    if profile:
        rprint(f"Profiling source table {fqn_fmt}...")
        args = {"schema": schema, "relation_name": table}
        content = run_dbt_operation(
            "print_profile_docs", args=args, target=target, quiet=True
        )
        success_msg = f"Profile successfully written to {docs_path_fmt}."
    else:
        rprint(f"Creating description template for model [blue]{fqn_fmt}[/blue]...")
        args = {"schema": schema, "relation_name": table}
        content = run_dbt_operation(
            "create_description_markdown", args=args, target=target, quiet=True
        )
        success_msg = f"Description template successfully written to {docs_path_fmt}."

    with docs_path.open("w") as file:
        file.write(content)

    rprint(success_msg)

    if not non_interactive:
        rprint(
            Panel(
                f"""Before continuing, please open [link={docs_path}]{table}.md[/link]
    and add your description in the [blue]📝 Details[/blue] section.""",
                title="ATTENTION",
                width=100,
            )
        )
        Prompt.ask("Press [green]ENTER[/green] to continue")


@app.command()
def create(
    ctx: typer.Context,  # noqa: ARG001
    source: Annotated[
        str, typer.Argument(help="The name of the source schema.", show_default=False)
    ],
    schema_path: Annotated[
        str | None,
        typer.Option(
            "--schema-path",
            help="""The path to the source YAML.
        Defaults to `{PROJECT_DIR}/models/sources/{source}.yml`.""",
        ),
    ] = None,
    case_sensitive_cols: Annotated[
        bool | None,
        typer.Option(
            "--case-sensitive-cols",
            "-c",
            help="Whether the column names of the source are case-sensitive.",
        ),
    ] = True,
    profile: Annotated[
        bool | None,
        typer.Option(
            "--profile/--no-profile",
            "-p/-np",
            help="Whether to skip table profiling.",
        ),
    ] = False,
    env: options.environment = config.default_env,
    project: options.project = config.project_name,
    force: options.force("Overwrite the existing source.") = False,
) -> bool:
    """Add a new source schema with all existing tables in it."""
    dbt_project_dir = Path(context.get("PROJECT_DIR"))

    if not project:
        project = dbt_project_dir.name

    base_dir = dbt_project_dir / "models" / "sources" / source

    if not schema_path:
        schema_path: Path = base_dir / f"{source}.yml"

    if not base_dir.exists():
        base_dir.mkdir(parents=True, exist_ok=True)

    source_exists = check_if_source_exists(source, schema_path=schema_path)
    if source_exists:
        if force:
            operation = "overwriting"
        else:
            rprint(f"Source [blue]{source}[/blue] [b]already exists[/b]. Skipping...")
            return False
    else:
        operation = "creating"

    rprint(f"[white]{operation.title()} source[/white] [blue]{source}[/blue]...")

    args = {"schema_name": source, "print_result": True}
    existing_tables_str = run_dbt_operation(
        "get_tables_in_schema", args=args, target=env, quiet=True
    )
    if not existing_tables_str:
        msg = f"Schema '{source}' is empty."
        raise ValueError(msg)
    existing_tables = existing_tables_str.split(",")

    for table in existing_tables:
        _create_table_docs(
            base_dir=base_dir,
            schema=source,
            table=table,
            profile=profile,  # type: ignore
            target=env,
        )

    # Generate the YAML file.
    args = {"schema_name": source, "case_sensitive_cols": case_sensitive_cols}
    source_str = run_dbt_operation("generate_source", args=args, target=env, quiet=True)

    with Path(schema_path).open("w") as f:
        f.write(source_str)

    # Print success message.
    operation_past_tenses = {"overwriting": "overwritten", "creating": "created"}
    operation_past_tense = operation_past_tenses[operation]
    rprint(
        f"Source [blue]{source}[/blue] has been {operation_past_tense} successfully."
    )

    return True


@app.command()
def add(
    ctx: typer.Context,  # noqa: ARG001
    table_name: Annotated[
        str, typer.Argument(help="The name of the table to add.", show_default=False)
    ],
    case_sensitive_cols: Annotated[
        bool | None,
        typer.Option(
            "--case-sensitive-cols",
            "-c",
            help="Whether the column names are case-sensitive.",
        ),
    ] = True,
    profile: Annotated[
        bool | None,
        typer.Option(
            "--profile/--no-profile",
            "-p/-np",
            help="Whether to document data profiling information.",
        ),
    ] = False,
    project: options.project = config.project_name,
    env: options.environment = config.default_env,
    non_interactive: Annotated[
        bool | None,
        typer.Option(
            "--non-interactive",
            "-ni",
            help="Whether to execute the command without interactive prompts.",
        ),
    ] = False,
) -> bool:
    """Add a new table to a source schema and materializes it as a base model."""
    dbt_project_dir = Path(context.get("PROJECT_DIR"))
    project = project or dbt_project_dir.name
    source = config.bronze_schema

    base_dir = dbt_project_dir.joinpath("models", "sources", source)

    if not base_dir.exists():
        base_dir.mkdir(parents=True, exist_ok=True)

    schema_path = _get_default_schema_path(source)
    fqn = f"{source}.{table_name}"
    fqn_fmt = f"[white]{source}.{table_name}[/white]"

    yaml_exists = check_if_source_table_exists(source=source, table_name=table_name)
    if yaml_exists:
        rprint(f"Source table '{fqn}' already exists. Skipping...")
        return False

    table_exists = check_if_relation_exists(name=table_name, schema=source, target=env)
    if not table_exists:
        msg = f"Table '{fqn}' does not exist in the database schema '{source}' on target '{env}'."
        raise ValueError(msg)

    # Generate docs.
    _create_table_docs(
        base_dir=base_dir,
        schema=source,
        table=table_name,
        profile=profile,
        target=env,
        non_interactive=non_interactive,
    )

    # Generate source YAML and append it to the sources schema.
    args = {
        "schema_name": source,
        "table_names": [table_name],
        "case_sensitive_cols": case_sensitive_cols,
    }
    source_str = run_dbt_operation("generate_source", args=args, target=env, quiet=True)

    # Special case when adding the first table.
    has_tables = False
    # The "tables" key is at the top of the props file, so no need to scan
    # the entire file (it could have millions of rows).
    tables_key_scan_limit = 100
    with schema_path.open() as file:
        for line_number, line in enumerate(file):
            if "tables" in line:
                has_tables = True
                break
            if line_number > tables_key_scan_limit:
                break
    if not has_tables:
        source_str = "\n" + indent("tables:", " " * 4) + source_str

    with schema_path.open("a") as file:
        file.write(source_str)

    rprint(f"Source table {fqn_fmt} has been added successfully.")

    schema_path_trimmed = schema_path.relative_to(
        schema_path.parent.parent.parent.parent
    )

    if not non_interactive:
        rprint(
            Panel(
                f"""Before continuing, please provide the source table's metadata in [link={schema_path}]{schema_path_trimmed}[/link]
    (owners, tests, etc.).""",
                title="ATTENTION",
                width=120,
            )
        )

        Prompt.ask("Press [green]ENTER[/green] to continue")

    return True


@app.command(context_settings=wrapper_context_settings)
def freshness(
    ctx: typer.Context,
    select: Annotated[
        str | None, typer.Option("--select", "-s", help="The source(s) to select.")
    ] = None,
    env: options.environment = config.default_env,
) -> str:
    """Validate the freshness of source table(s)."""
    dbt_project = get_current_dbt_project_obj(target=env)

    args = []
    if select:
        if "." not in select:
            # Table name has to be fully qualified.
            select = f"{config.bronze_schema}.{select}"
        if "source:" not in select:
            select = f"source:{select}"
        args.extend(["-s", select])
    if ctx.args:
        args.extend(ctx.args)

    # Call dbt source freshness using dbt-core-interface
    result = dbt_project.source_freshness(*args)

    if not result.success:
        exception = result.exception or "unknown error"
        msg = f"dbt source freshness failed: {exception}"
        raise RuntimeError(msg)

    # Return the result for the test to verify
    return "PASS" if result.success else "FAIL"


@app.command()
def rm(
    table_name: Annotated[
        str, typer.Argument(help="The name of the table to add.", show_default=False)
    ],
    remove_base_model: Annotated[
        bool | None,
        typer.Option(
            "--remove-base-model",
            "-b",
            help="Whether to remove the corresponding base model.",
        ),
    ] = False,
    env: options.environment = config.default_env,
) -> bool:
    """Remove a source table from the schema YAML."""
    dbt_project_dir = Path(context.get("PROJECT_DIR"))
    source = config.bronze_schema
    base_dir = dbt_project_dir.joinpath("models", "sources", source)
    schema_path = _get_default_schema_path(source)

    # Remove the description Markdown.
    description_markdown = base_dir / f"{table_name}.md"
    description_markdown.unlink(missing_ok=True)

    # Remove the definition from source schema YAML.
    with schema_path.open() as file:
        cfg = yaml.load(file)

    try:
        source_cfg = next(iter(s for s in cfg["sources"] if s["name"] == source))
    except StopIteration as e:
        msg = f"Source table {table_name} not found in {schema_path}."
        raise ValueError(msg) from e

    source_cfg["tables"] = [t for t in source_cfg["tables"] if t["name"] != table_name]

    with schema_path.open("w") as file:
        yaml.dump(cfg, file)

    # Remove the base model.
    if remove_base_model:
        base_model_name = config.silver_schema_prefix + "_" + table_name
        base_model_rm(name=base_model_name, drop_relation=True, env=env)

    return True


if __name__ == "__main__":
    app()
