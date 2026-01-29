import json
from pathlib import Path
import shutil
from unittest.mock import Mock

import pytest

from nesso_cli.models import context
from nesso_cli.models.base_model import (
    bootstrap_yaml as base_model_bootstrap_yaml,
)
from nesso_cli.models.base_model import (
    check_if_base_model_exists,
)
from nesso_cli.models.common import call_shell, execute_sql
from nesso_cli.models.config import config
from nesso_cli.models.model import bootstrap_yaml as model_bootstrap_yaml
from nesso_cli.models.seed import check_if_seed_exists
from nesso_cli.models.seed import register as seed_register
from nesso_cli.models.source import (
    add as source_add,
)
from nesso_cli.models.source import (
    check_if_source_exists,
    check_if_source_table_exists,
)
from nesso_cli.models.tests.test_source import create_empty_source


PROJECT_DIR = Path(__file__).parent.parent.joinpath("dbt_projects", "duckdb")
context._set("PROJECT_DIR", PROJECT_DIR)
TEST_SEED_COUNTRIES_NAME = "countries_example"


@pytest.fixture
def create_seed(TEST_SCHEMA):
    # Create seed
    seed_schema_path = PROJECT_DIR.joinpath("seeds", "schema.yml")

    seed_register(
        seed=TEST_SEED_COUNTRIES_NAME,
        schema_path=seed_schema_path,
        technical_owner="test_technical_owner",
        business_owner="test_business_owner",
    )

    # Check if the schema file was created.
    assert seed_schema_path.exists()

    # Check if the seed was materialized.
    execute_sql(f"SELECT * FROM {TEST_SCHEMA}.{TEST_SEED_COUNTRIES_NAME}")

    # Check if the seed was added to the schema file.
    assert check_if_seed_exists(TEST_SEED_COUNTRIES_NAME, schema_path=seed_schema_path)

    yield

    # Cleanup.
    seed_schema_path.unlink()
    execute_sql(
        f"DROP TABLE IF EXISTS {TEST_SCHEMA}.{TEST_SEED_COUNTRIES_NAME};", commit=True
    )


@pytest.fixture
def create_source(
    create_accounts_table,
    TEST_SOURCE,
    SOURCE_SCHEMA_PATH,
    TEST_TABLE_ACCOUNT,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
):
    # Assumptions.
    assert not check_if_source_exists(TEST_SOURCE)
    assert not check_if_source_table_exists(TEST_SOURCE, TEST_TABLE_ACCOUNT)
    assert not check_if_base_model_exists(TEST_TABLE_ACCOUNT_BASE_MODEL)

    create_empty_source(TEST_SOURCE, SOURCE_SCHEMA_PATH)

    assert check_if_source_exists(TEST_SOURCE)

    # Add a table with a base model.
    mock_ctx = Mock()
    mock_ctx.args = []
    source_add(
        ctx=mock_ctx,
        table_name=TEST_TABLE_ACCOUNT,
        project=PROJECT_DIR.name,
        non_interactive=True,
    )

    assert check_if_source_table_exists(TEST_SOURCE, TEST_TABLE_ACCOUNT)

    yield

    # Cleanup.
    shutil.rmtree(
        PROJECT_DIR.joinpath("models", "sources", TEST_SOURCE),
        ignore_errors=True,
    )


@pytest.fixture
def create_base_model(
    TEST_SCHEMA,
    TEST_SOURCE,
    TEST_TABLE_ACCOUNT,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
):
    base_model_path = (
        PROJECT_DIR / "models" / config.silver_schema / TEST_TABLE_ACCOUNT_BASE_MODEL
    )
    base_model_file_sql = base_model_path / f"{TEST_TABLE_ACCOUNT_BASE_MODEL}.sql"
    base_model_path.mkdir(parents=True, exist_ok=True)
    with Path(base_model_file_sql).open("w") as f:
        f.write(
            f"select * from {{{{ source('{TEST_SOURCE}', '{TEST_TABLE_ACCOUNT}') }}}}"
        )
    # Bootstrap YAML for the model.
    mock_ctx = Mock()
    mock_ctx.args = []
    base_model_bootstrap_yaml(
        ctx=mock_ctx,
        base_model_name=TEST_TABLE_ACCOUNT,
    )
    assert check_if_base_model_exists(TEST_TABLE_ACCOUNT_BASE_MODEL)

    yield

    # Cleanup.
    shutil.rmtree(
        PROJECT_DIR.joinpath("models", config.silver_schema),
        ignore_errors=False,
    )
    execute_sql(
        f"DROP VIEW IF EXISTS {TEST_SCHEMA}.{TEST_TABLE_ACCOUNT_BASE_MODEL} CASCADE",
        commit=True,
    )


@pytest.fixture
def create_model(
    create_source,
    create_base_model,
    TEST_TABLE_ACCOUNT,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
):
    # Create model SQL.
    model_path = PROJECT_DIR.joinpath(
        "models",
        config.gold_layer_name,
        "test_mart",
        "test_project",
        TEST_TABLE_ACCOUNT,
        TEST_TABLE_ACCOUNT + ".sql",
    )
    model_path.parent.mkdir(parents=True, exist_ok=True)

    with Path(model_path).open("w") as f:
        f.write(f"""SELECT * FROM {{{{ ref("{TEST_TABLE_ACCOUNT_BASE_MODEL}") }}}}""")

    # Bootstrap YAML for the model.
    mock_ctx = Mock()
    mock_ctx.args = []
    model_bootstrap_yaml(
        ctx=mock_ctx,
        model=TEST_TABLE_ACCOUNT,
    )

    yield

    # Cleanup.
    shutil.rmtree(
        PROJECT_DIR.joinpath("models", config.gold_layer_name), ignore_errors=True
    )


@pytest.fixture
def create_manifest() -> None:
    """Run dbt commands in a specific order to generate the manifest.json file."""
    manifest_path = PROJECT_DIR.joinpath("target", "manifest.json")
    manifest_path.unlink(missing_ok=True)

    call_shell("dbt clean")
    call_shell("dbt deps")

    # fix https://github.com/dbt-labs/dbt-utils/issues/627
    shutil.rmtree(
        PROJECT_DIR.joinpath(
            "dbt_packages",
            "dbt_utils",
            "tests",
        ),
        ignore_errors=True,
    )

    run_results = call_shell("dbt run")
    test_results = call_shell("dbt test")
    freshness_results = call_shell("dbt source freshness")
    docs_results = call_shell("dbt docs generate")

    assert run_results is not None
    assert test_results is not None
    assert freshness_results is not None
    assert docs_results is not None

    assert manifest_path.exists()

    yield

    # Cleanup.
    manifest_path.unlink()


def test_manifest(
    create_manifest,
    create_seed,
    create_model,
    TEST_SOURCE,
    TEST_SCHEMA,
    TEST_TABLE_ACCOUNT,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
):
    """Verify that the manifest.json file contains the expected metadata.

    The test has 3 stages:
    1. Create resources of each type (seed, source, base model, model).
    2. Run dbt commands in a specific order to generate the manifest.json file.
    3. Inspect that the results for each resource match expectations.
    """

    with Path(PROJECT_DIR.joinpath("target", "manifest.json")).open() as f:
        manifest = json.load(f)

    # Tests.
    # Seed.
    seed_metadata = manifest["nodes"][f"seed.duckdb.{TEST_SEED_COUNTRIES_NAME}"]
    assert seed_metadata["schema"] == TEST_SCHEMA

    # Source table.
    source_table_fqn = f"{TEST_SOURCE}.{TEST_TABLE_ACCOUNT}"
    source_metadata = manifest["sources"][f"source.duckdb.{source_table_fqn}"]
    assert source_metadata["schema"] == TEST_SOURCE

    # Base model.
    base_model_metadata = manifest["nodes"][
        f"model.duckdb.{TEST_TABLE_ACCOUNT_BASE_MODEL}"
    ]
    assert base_model_metadata["schema"] == TEST_SCHEMA

    # Model.
    model_metadata = manifest["nodes"][f"model.duckdb.{TEST_TABLE_ACCOUNT}"]
    assert model_metadata["schema"] == TEST_SCHEMA
