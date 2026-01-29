from pathlib import Path

import nesso_cli.models.context as context
import pytest
from nesso_cli.models.models import DBTProperties
from nesso_cli.models.common import execute_sql
from nesso_cli.models.config import config
from typer.testing import CliRunner
from nesso_cli.models.update import model as update_model, base_model as update_base_model, source as update_source

PROJECT_DIR = Path(__file__).parent.joinpath("dbt_projects", "duckdb")
context._set("PROJECT_DIR", PROJECT_DIR)

runner = CliRunner()

YAML_SOURCE_COLUMNS = {
    "id": "BIGINT",
    "name": "CHARACTER VARYING(256)",
    "email": "CHARACTER VARYING(256)",
    "mobile": "CHARACTER VARYING(256)",
    "country": "CHARACTER VARYING(256)",
    "_viadot_downloaded_at_utc": "TIMESTAMP WITH TIME ZONE",
}

YAML_SOURCE_COLUMNS_METADATA = {
    "id": {
        "quote": True,
        "data_type": "BIGINT",
        "description": "description_id",
        "data_tests": ["not_null"],
        "tags": ["uat"],
    },
    "name": {
        "quote": True,
        "data_type": "CHARACTER VARYING(256)",
        "description": "description_name",
        "data_tests": ["not_null"],
        "tags": ["uat"],
    },
    "email": {
        "quote": True,
        "data_type": "CHARACTER VARYING(256)",
        "description": "description_email",
        "data_tests": ["unique", "not_null", {"dbt_utils.expression_is_true": {"expression": "LIKE '%@%'"}}],
        "tags": ["uat"],
    },
    "mobile": {
        "quote": True,
        "data_type": "CHARACTER VARYING(256)",
        "description": "description_mobile",
        "tags": ["uat"],
    },
    "country": {
        "quote": True,
        "data_type": "CHARACTER VARYING(256)",
        "description": "description_country",
        "tags": ["uat"],
    },
    "_viadot_downloaded_at_utc": {
        "quote": True,
        "data_type": "TIMESTAMP WITH TIME ZONE",
        "description": "description_viadot_downloaded_at_utc",
        "tags": ["uat"],
    },
}


COLUMNS_AFTER_INSERT = {
    "id": {
        "quote": True,
        "data_type": "BIGINT",
        "description": "description_id",
        "data_tests": ["not_null"],
        "tags": ["uat"],
    },
    "name": {
        "quote": True,
        "data_type": "CHARACTER VARYING(256)",
        "description": "description_name",
        "data_tests": ["not_null"],
        "tags": ["uat"],
    },
    "email": {
        "quote": True,
        "data_type": "CHARACTER VARYING(256)",
        "description": "description_email",
        "data_tests": ["unique", "not_null", {"dbt_utils.expression_is_true": {"expression": "LIKE '%@%'"}}],
        "tags": ["uat"],
    },
    "mobile": {
        "quote": True,
        "data_type": "CHARACTER VARYING(256)",
        "description": "description_mobile",
        "tags": ["uat"],
    },
    "country": {
        "quote": True,
        "data_type": "CHARACTER VARYING(256)",
        "description": "description_country",
        "tags": ["uat"],
    },
    "_viadot_downloaded_at_utc": {
        "quote": True,
        "data_type": "TIMESTAMP WITH TIME ZONE",
        "description": "description_viadot_downloaded_at_utc",
        "tags": ["uat"],
    },
    "new_column_name": {
        "quote": True,
        "data_type": "CHARACTER VARYING(256)",
        "description": "",
        "tags": [],
    },
}
COLUMNS_AFTER_DELETE = {
    "id": {
        "quote": True,
        "data_type": "BIGINT",
        "description": "description_id",
        "data_tests": ["not_null"],
        "tags": ["uat"],
    },
    "name": {
        "quote": True,
        "data_type": "CHARACTER VARYING(256)",
        "description": "description_name",
        "data_tests": ["not_null"],
        "tags": ["uat"],
    },
    "email": {
        "quote": True,
        "data_type": "CHARACTER VARYING(256)",
        "description": "description_email",
        "data_tests": ["unique", "not_null", {"dbt_utils.expression_is_true": {"expression": "LIKE '%@%'"}}],
        "tags": ["uat"],
    },
    "mobile": {
        "quote": True,
        "data_type": "CHARACTER VARYING(256)",
        "description": "description_mobile",
        "tags": ["uat"],
    },
    "country": {
        "quote": True,
        "data_type": "CHARACTER VARYING(256)",
        "description": "description_country",
        "tags": ["uat"],
    },
}

COLUMNS_AFTER_UPDATE = {
    "id": {
        "quote": True,
        "data_type": "BIGINT",
        "description": "description_id",
        "data_tests": ["not_null"],
        "tags": ["uat"],
    },
    "name": {
        "quote": True,
        "data_type": "CHARACTER VARYING(256)",
        "description": "description_name",
        "data_tests": ["not_null"],
        "tags": ["uat"],
    },
    "email": {
        "quote": True,
        "data_type": "CHARACTER VARYING(256)",
        "description": "description_email",
        "data_tests": ["unique", "not_null", {"dbt_utils.expression_is_true": {"expression": "LIKE '%@%'"}}],
        "tags": ["uat"],
    },
    "mobile": {
        "quote": True,
        "data_type": "CHARACTER VARYING(256)",
        "description": "description_mobile",
        "tags": ["uat"],
    },
    "new_updated_name": {
        "quote": True,
        "data_type": "CHARACTER VARYING(256)",
        "description": "",
        "tags": [],
    },
    "_viadot_downloaded_at_utc": {
        "quote": True,
        "data_type": "TIMESTAMP WITH TIME ZONE",
        "description": "description_viadot_downloaded_at_utc",
        "tags": ["uat"],
    },
}

COLUMNS_AFTER_UPDATE_DATA_TYPE = {
    "id": {
        "quote": True,
        "data_type": "BIGINT",
        "description": "description_id",
        "data_tests": ["not_null"],
        "tags": ["uat"],
    },
    "name": {
        "quote": True,
        "data_type": "CHARACTER VARYING(256)",
        "description": "description_name",
        "data_tests": ["not_null"],
        "tags": ["uat"],
    },
    "email": {
        "quote": True,
        "data_type": "CHARACTER VARYING(256)",
        "description": "description_email",
        "data_tests": ["unique", "not_null", {"dbt_utils.expression_is_true": {"expression": "LIKE '%@%'"}}],
        "tags": ["uat"],
    },
    "mobile": {
        "quote": True,
        "data_type": "CHARACTER VARYING(256)",
        "description": "description_mobile",
        "tags": ["uat"],
    },
    "country": {
        "quote": True,
        "data_type": "CHARACTER VARYING(256)",
        "description": "description_country",
        "tags": ["uat"],
    },
    "_viadot_downloaded_at_utc": {
        "quote": True,
        "data_type": "TIMESTAMP WITH TIME ZONE",
        "description": "description_viadot_downloaded_at_utc",
        "tags": ["uat"],
    },
}

ADD_COLUMN = "ADD COLUMN new_column_name VARCHAR(256)"
DELETE_COLUMN = "DROP COLUMN _viadot_downloaded_at_utc CASCADE"
UPDATE_COLUMN = "RENAME COLUMN country TO new_updated_name"
UPDATE_COLUMN_DATA_TYPE = "ALTER COLUMN mobile TYPE VARCHAR(256);"


@pytest.fixture(params=[ADD_COLUMN])
def setup_models_in_db(
    request,
    create_accounts_table,
    TEST_SOURCE,
    TEST_SCHEMA,
    TEST_TABLE_ACCOUNT,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
    MODEL,
):
    # Definitions of the source, base model, and model.
    source_fqn = f"{TEST_SOURCE}.{TEST_TABLE_ACCOUNT}"
    base_model_fqn = f"{TEST_SCHEMA}.{TEST_TABLE_ACCOUNT_BASE_MODEL}"
    model_fqn = f"{TEST_SCHEMA}.{MODEL}"

    # Creates tables and views mimicking the source, base model, and model.
    execute_sql(f"CREATE SCHEMA IF NOT EXISTS {TEST_SCHEMA}", commit=True, target="dev")
    execute_sql(f"DROP VIEW IF EXISTS {base_model_fqn} CASCADE", commit=True, target="dev")
    execute_sql(f"ALTER TABLE {source_fqn} {request.param}", commit=True, target="dev")
    execute_sql(f"CREATE OR REPLACE VIEW {base_model_fqn} AS SELECT * FROM {source_fqn}", commit=True, target="dev")
    execute_sql(f"CREATE OR REPLACE VIEW {model_fqn} AS SELECT * FROM {base_model_fqn}", commit=True, target="dev")

    yield

    # Cleaning.
    execute_sql(f"DROP TABLE IF EXISTS {source_fqn} CASCADE", commit=True, target="dev")


def test_update_model_create_new_column(
    setup_model,
    setup_models_in_db,
    MODEL,
):
    # Assumptions.
    yaml_columns_metadata = DBTProperties(file_path=setup_model).get_yaml_table_columns(
        MODEL
    )
    assert yaml_columns_metadata != COLUMNS_AFTER_INSERT

    # Call the function directly
    update_model(model=MODEL)

    yaml_columns_metadata = DBTProperties(file_path=setup_model).get_yaml_table_columns(
        MODEL
    )

    assert yaml_columns_metadata == COLUMNS_AFTER_INSERT


@pytest.mark.parametrize("setup_models_in_db", [UPDATE_COLUMN], indirect=True)
def test_update_model_update_column(
    setup_model,
    setup_models_in_db,
    MODEL,
):
    # Assumptions.
    yaml_columns_metadata = DBTProperties(file_path=setup_model).get_yaml_table_columns(
        MODEL
    )
    assert yaml_columns_metadata != COLUMNS_AFTER_UPDATE

    # Call the function directly
    update_model(model=MODEL)

    yaml_columns_metadata = DBTProperties(file_path=setup_model).get_yaml_table_columns(
        MODEL
    )

    assert yaml_columns_metadata == COLUMNS_AFTER_UPDATE


@pytest.mark.parametrize("setup_models_in_db", [DELETE_COLUMN], indirect=True)
def test_update_model_delete_column(
    setup_model,
    setup_models_in_db,
    MODEL,
):
    # Assumptions.
    yaml_columns_metadata = DBTProperties(file_path=setup_model).get_yaml_table_columns(
        MODEL
    )
    assert yaml_columns_metadata != COLUMNS_AFTER_DELETE

    # Call the function directly
    update_model(model=MODEL)

    yaml_columns_metadata = DBTProperties(file_path=setup_model).get_yaml_table_columns(
        MODEL
    )

    assert yaml_columns_metadata == COLUMNS_AFTER_DELETE


@pytest.mark.parametrize("setup_models_in_db", [UPDATE_COLUMN_DATA_TYPE], indirect=True)
def test_update_model_column_data_type(
    setup_model,
    setup_models_in_db,
    MODEL,
):
    # Assumptions.
    yaml_columns_metadata = DBTProperties(file_path=setup_model).get_yaml_table_columns(
        MODEL
    )
    yaml_columns_metadata["country"]["data_type"] = "FAKE_DATA_TYPE"
    assert yaml_columns_metadata != COLUMNS_AFTER_UPDATE_DATA_TYPE

    # Call the function directly
    update_model(model=MODEL)

    yaml_columns_metadata = DBTProperties(file_path=setup_model).get_yaml_table_columns(
        MODEL
    )

    assert yaml_columns_metadata == COLUMNS_AFTER_UPDATE_DATA_TYPE


def test_update_base_model_create_new_column(
    setup_base_model,
    setup_models_in_db,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
):
    # Assumptions.
    yaml_columns_metadata = DBTProperties(
        file_path=setup_base_model
    ).get_yaml_table_columns(TEST_TABLE_ACCOUNT_BASE_MODEL)
    assert yaml_columns_metadata != COLUMNS_AFTER_INSERT

    # Call the function directly
    update_base_model(base_model=TEST_TABLE_ACCOUNT_BASE_MODEL)

    yaml_columns_metadata = DBTProperties(
        file_path=setup_base_model
    ).get_yaml_table_columns(TEST_TABLE_ACCOUNT_BASE_MODEL)

    assert yaml_columns_metadata == COLUMNS_AFTER_INSERT


@pytest.mark.parametrize("setup_models_in_db", [UPDATE_COLUMN], indirect=True)
def test_update_base_model_update_column(
    setup_base_model,
    setup_models_in_db,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
):
    # Assumptions.
    yaml_columns_metadata = DBTProperties(
        file_path=setup_base_model
    ).get_yaml_table_columns(TEST_TABLE_ACCOUNT_BASE_MODEL)
    assert yaml_columns_metadata != COLUMNS_AFTER_UPDATE

    # Call the function directly
    update_base_model(base_model=TEST_TABLE_ACCOUNT_BASE_MODEL)

    yaml_columns_metadata = DBTProperties(
        file_path=setup_base_model
    ).get_yaml_table_columns(TEST_TABLE_ACCOUNT_BASE_MODEL)

    assert yaml_columns_metadata == COLUMNS_AFTER_UPDATE


@pytest.mark.parametrize("setup_models_in_db", [DELETE_COLUMN], indirect=True)
def test_update_base_model_delete_column(
    setup_base_model,
    setup_models_in_db,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
):
    # Assumptions.
    yaml_columns_metadata = DBTProperties(
        file_path=setup_base_model
    ).get_yaml_table_columns(TEST_TABLE_ACCOUNT_BASE_MODEL)
    assert yaml_columns_metadata != COLUMNS_AFTER_DELETE

    # Call the function directly
    update_base_model(base_model=TEST_TABLE_ACCOUNT_BASE_MODEL)

    yaml_columns_metadata = DBTProperties(
        file_path=setup_base_model
    ).get_yaml_table_columns(TEST_TABLE_ACCOUNT_BASE_MODEL)
    assert yaml_columns_metadata == COLUMNS_AFTER_DELETE


@pytest.mark.parametrize("setup_models_in_db", [UPDATE_COLUMN_DATA_TYPE], indirect=True)
def test_update_base_model_column_data_type(
    setup_base_model,
    setup_models_in_db,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
):
    # Assumptions.
    yaml_columns_metadata = DBTProperties(
        file_path=setup_base_model
    ).get_yaml_table_columns(TEST_TABLE_ACCOUNT_BASE_MODEL)
    yaml_columns_metadata["mobile"]["data_type"] = "FAKE_DATA_TYPE"
    assert yaml_columns_metadata != COLUMNS_AFTER_UPDATE_DATA_TYPE

    # Call the function directly
    update_base_model(base_model=TEST_TABLE_ACCOUNT_BASE_MODEL)

    yaml_columns_metadata = DBTProperties(
        file_path=setup_base_model
    ).get_yaml_table_columns(TEST_TABLE_ACCOUNT_BASE_MODEL)

    assert yaml_columns_metadata == COLUMNS_AFTER_UPDATE_DATA_TYPE


def test_update_source_create_new_column(
    setup_source, setup_models_in_db, TEST_TABLE_ACCOUNT
):
    # Assumptions.
    yaml_columns_metadata = DBTProperties(
        file_path=setup_source
    ).get_yaml_table_columns(TEST_TABLE_ACCOUNT)
    assert yaml_columns_metadata != COLUMNS_AFTER_INSERT

    # Call the function directly
    update_source(table_name=TEST_TABLE_ACCOUNT)

    yaml_columns_metadata = DBTProperties(
        file_path=setup_source
    ).get_yaml_table_columns(TEST_TABLE_ACCOUNT)

    assert yaml_columns_metadata == COLUMNS_AFTER_INSERT


@pytest.mark.parametrize("setup_models_in_db", [UPDATE_COLUMN], indirect=True)
def test_update_source_update_column(
    setup_source, setup_models_in_db, TEST_TABLE_ACCOUNT
):
    # Assumptions.
    yaml_columns_metadata = DBTProperties(
        file_path=setup_source
    ).get_yaml_table_columns(TEST_TABLE_ACCOUNT)
    assert yaml_columns_metadata != COLUMNS_AFTER_UPDATE

    # Call the function directly
    update_source(table_name=TEST_TABLE_ACCOUNT)

    yaml_columns_metadata = DBTProperties(
        file_path=setup_source
    ).get_yaml_table_columns(TEST_TABLE_ACCOUNT)

    assert yaml_columns_metadata == COLUMNS_AFTER_UPDATE


@pytest.mark.parametrize("setup_models_in_db", [DELETE_COLUMN], indirect=True)
def test_update_source_delete_column(
    setup_source,
    setup_models_in_db,
    TEST_SOURCE,
    TEST_TABLE_ACCOUNT,
):
    # Assumptions.
    yaml_columns_metadata = DBTProperties(
        file_path=setup_source
    ).get_yaml_table_columns(TEST_TABLE_ACCOUNT)
    assert yaml_columns_metadata != COLUMNS_AFTER_DELETE

    # Call the function directly
    update_source(table_name=TEST_TABLE_ACCOUNT, schema=TEST_SOURCE)

    yaml_columns_metadata = DBTProperties(
        file_path=setup_source
    ).get_yaml_table_columns(TEST_TABLE_ACCOUNT)

    assert yaml_columns_metadata == COLUMNS_AFTER_DELETE


@pytest.mark.parametrize("setup_models_in_db", [UPDATE_COLUMN_DATA_TYPE], indirect=True)
def test_update_source_update_column_data_type(
    setup_source, setup_models_in_db, TEST_SOURCE, TEST_TABLE_ACCOUNT
):
    # Assumptions.
    yaml_columns_metadata = DBTProperties(
        file_path=setup_source
    ).get_yaml_table_columns(TEST_TABLE_ACCOUNT)
    yaml_columns_metadata["mobile"]["data_type"] = "FAKE_DATA_TYPE"
    assert yaml_columns_metadata != COLUMNS_AFTER_UPDATE_DATA_TYPE

    # Call the function directly
    update_source(table_name=TEST_TABLE_ACCOUNT, schema=TEST_SOURCE)

    yaml_columns_metadata = DBTProperties(
        file_path=setup_source
    ).get_yaml_table_columns(TEST_TABLE_ACCOUNT)

    assert yaml_columns_metadata == COLUMNS_AFTER_UPDATE_DATA_TYPE
