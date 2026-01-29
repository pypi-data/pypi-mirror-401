from pathlib import Path
from unittest.mock import Mock

import nesso_cli.models.context as context
from nesso_cli.models.main import debug as dbt_debug
from nesso_cli.models.main import run as dbt_run
from nesso_cli.models.main import setup as dbt_setup
from nesso_cli.models.main import test as dbt_test


PROJECT_DIR = Path(__file__).parent.joinpath("dbt_projects", "duckdb")
context._set("PROJECT_DIR", PROJECT_DIR)


def test_test(setup_model, MODEL):
    # Create mock context
    mock_ctx = Mock()
    mock_ctx.args = []

    # Call the function directly
    dbt_test(ctx=mock_ctx, select=MODEL, env="dev")


def test_debug():
    # Create mock context
    mock_ctx = Mock()
    mock_ctx.args = []

    # Call the function directly
    dbt_debug(ctx=mock_ctx, env="dev")


def test_run(setup_model, MODEL):
    # Create mock context
    mock_ctx = Mock()
    mock_ctx.args = []

    # Call the function directly
    dbt_run(ctx=mock_ctx, select=MODEL, env="dev")


def test_setup():
    dbt_erroring_dir_path = PROJECT_DIR.joinpath(
        "dbt_packages",
        "dbt_utils",
        "tests",
    )

    # Call the function directly
    dbt_setup()

    assert not dbt_erroring_dir_path.exists()
