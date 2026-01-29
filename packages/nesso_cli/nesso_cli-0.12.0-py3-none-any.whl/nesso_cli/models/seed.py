"""Nesso models seeds management.

In order to avoid confusion, it's useful to distinguish between these four entities:

a) seed file
A CSV file that is used by dbt to create a source table. We extend that functionality
to also support Excel files.

b) seed
A dbt concept which allows to upload CSVs as tables. In this file, we use this word
to refer to an entry in the seed schema about a particular seed file.

c) seed schema
The YAML file holding metadata about seed tables.

d) seed table
The materialized seed, ie. the actual database table created based on the seed file.

Therefore, to check if a seed exists, we'll be looking for a relevant entry in the
seed schema. To check if a seed table exists, we will be checking in the database.
And to check if the seed file or seed schema exists, we'll be examining or searching
for YAML files.
"""

from pathlib import Path
from typing import Annotated

from loguru import logger
from rich import print as rprint

# import pandas as pd
import typer

from nesso_cli.models import context
from nesso_cli.models.common import (
    check_if_relation_exists,
    get_current_dbt_project_obj,
    get_local_schema,
    options,
    run_dbt_operation,
)
from nesso_cli.models.config import config, yaml


app = typer.Typer()


# def _excel_to_csv(infile: Union[str, Path], outfile: Union[str, Path]) -> None:
#     """
#     Converts an Excel file to a CSV.

#     Args:
#         infile (Union[str, Path]): The path to the Excel file to be converted.
#         outfile (Union[str, Path]): The path where the CSV file should be saved.
#     """

#     df = pd.read_excel(infile)

#     # Sanitize column names.
#     df.columns = [f"{column.strip().replace(' ', '_')}" for column in df.columns]
#     df.columns = df.columns.str.replace("[,;{}()\n\t=]", "", regex=True)

#     df.to_csv(
#         outfile,
#         index=True,
#     )

#     # Enforce `pathlib.Path` type.
#     outfile = Path(outfile)
#     logger.debug(f"{outfile.name} has been created successfully.")


def check_if_schema_exists(schema_path: str | Path) -> bool:
    """Check if a seed schema file exists and is valid.

    Args:
        schema_path (str | Path): The path to the seed schema file.

    """
    schema_path = Path(schema_path)

    if not schema_path.exists():
        return False

    with schema_path.open() as f:
        schema_yaml = yaml.load(f)

    if schema_yaml is None:
        return False

    return "version" in schema_yaml and "seeds" in schema_yaml


def check_if_seed_exists(seed: str, schema_path: str | Path | None = None) -> bool:
    """Check if a seed is present in seed schema file.

    Args:
        seed (str): The name of the seed.
        schema_path (str | Path, optional): The path to the seed schema. Defaults to
            `DEFAULT_SEED_SCHEMA_PATH`.

    Returns:
        True if the seed is present in the schema, otherwise False.

    """
    if schema_path is None:
        schema_path = _get_default_schema_path()

    schema_path = Path(schema_path)

    if not schema_path.exists():
        return False

    with schema_path.open() as f:
        seeds = yaml.load(f)["seeds"]

    if not seeds:
        return False

    return any(s.get("name").lower() == seed.lower() for s in seeds)


def _get_default_schema_path() -> Path:
    dbt_project_dir = Path(context.get("PROJECT_DIR"))
    return dbt_project_dir / "seeds" / "schema.yml"


def create_schema(schema_path: str | Path) -> None:
    """Create a seed schema file.

    Args:
        schema_path (str | Path): The path where the seed schema file should be created.

    """
    schema_path = Path(schema_path)

    if schema_path.exists():
        msg = f"Schema '{schema_path}' already exists."
        raise ValueError(msg)

    # Run the macro and get clean output
    output = run_dbt_operation("generate_seed_schema_yaml", quiet=True)

    with schema_path.open("w") as f:
        f.write(output)


def add_to_schema(
    seed: str,
    schema_path: str | Path,
    technical_owner: str | None = None,
    business_owner: str | None = None,
    target: str | None = None,
    case_sensitive_cols: bool = True,
    overwrite: bool = False,
) -> None:
    """Add a seed entry to the seed schema file.

    Args:
        seed (str): The name of the seed to add.
        schema_path (str | Path): The path to the seed schema file.
        technical_owner (str | None, optional): The technical owner of the seed.
            Defaults to None.
        business_owner (str | None, optional): The business owner of the seed. Defaults
            to None.
        target (str | None, optional): The target environment. Defaults to None.
        case_sensitive_cols (bool, optional): Whether the seed columns are case
            sensitive. Defaults to True.
        overwrite (bool, optional): Whether to overwrite the seed metadata if it already
            exists. Defaults to False.

    """
    schema_exists = check_if_schema_exists(schema_path=schema_path)
    if schema_exists:
        if target == "prod":
            schema = config.bronze_schema
        else:
            schema = get_local_schema(target=target)
        fqn = f"{schema}.{seed}"

        # Check if the seed YAML is already present in the schema file.
        seed_yaml_exists = check_if_seed_exists(seed, schema_path=schema_path)
        if seed_yaml_exists and not overwrite:
            msg = (
                f"Seed YAML for {fqn} already exists and 'overwrite' is set to 'False'."
            )
            raise ValueError(msg)
    else:
        create_schema(schema_path)

    args = {
        "seed": seed,
        "technical_owner": technical_owner,
        "business_owner": business_owner,
        "case_sensitive_cols": case_sensitive_cols,
    }

    # Run the macro and get clean output
    seed_str = run_dbt_operation(
        "generate_seed_yaml", args=args, target=target, quiet=True
    )

    with Path(schema_path).open() as file:
        cfg = yaml.load(file)

    # Special case when adding the first seed - rewrite the whole file
    # to replace the inline empty list "seeds: []" with proper list format.
    seeds = cfg.get("seeds")
    if not seeds:
        seed_str = "version: 2\n\nseeds:\n" + seed_str
        mode = "w"
    else:
        mode = "a"

    with Path(schema_path).open(mode) as f:
        f.write(seed_str)

    successful_comment = f"Seed [blue]{seed}[/blue] has been successfully added to [white]{schema_path}[/white]."
    rprint(successful_comment)


@app.command()
def register(
    seed: Annotated[
        str,
        typer.Argument(help="The name of the seed to register.", show_default=False),
    ],
    technical_owner: options.technical_owner = None,
    business_owner: options.business_owner = None,
    schema_path: Annotated[
        str | None,
        typer.Option(
            "--yaml-path",
            help="""The absolute path of the schema file to which to append seed schema,
by default PROJECT_DIR/seeds/schema.yml""",
        ),
    ] = None,
    env: options.environment = config.default_env,
    force: options.force(
        """Whether to overwrite the seed metadata
        if it's is already present in the schema YAML."""
    ) = False,
) -> None:
    """Add an entry for the seed in seed schema and, if needed, materialize it."""
    if schema_path is None:
        schema_path = _get_default_schema_path()  # type: ignore

    schema_exists = check_if_schema_exists(schema_path=schema_path)  # type: ignore
    if schema_exists:
        schema = config.bronze_schema if env == "prod" else get_local_schema(target=env)

        # Check if the seed is already materialized in the database.
        seed_exists = check_if_relation_exists(name=seed, schema=schema)
        if seed_exists and not force:
            fqn = f"{schema}.{seed}"
            msg = f"Seed {fqn} is already materialized and 'force' is set to 'False'."
            raise ValueError(msg)
    else:
        create_schema(schema_path)  # type: ignore

    rprint(f"Registering seed [blue]{seed}[/blue]...")

    # Materialize the seed.
    dbt_project = get_current_dbt_project_obj(target=env)
    result = dbt_project.seed(select=[seed])

    if not result.success:
        msg = f"Seed file named '{seed}' was not found in the `seeds/` folder."
        raise ValueError(msg)

    logger.debug(f"Seed {seed} has been materialized successfully.")

    # Add it to seed schema.
    add_to_schema(
        seed,
        schema_path=schema_path,  # type: ignore
        technical_owner=technical_owner,
        business_owner=business_owner,
        target=env,
        overwrite=force,
    )

    rprint(f"Seed [blue]{seed}[/blue] has been registered [green]successfully[/green].")


if __name__ == "__main__":
    app()
