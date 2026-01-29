from test_update import (
    COLUMNS_AFTER_DELETE,
    COLUMNS_AFTER_INSERT,
    YAML_SOURCE_COLUMNS,
    YAML_SOURCE_COLUMNS_METADATA,
)
from nesso_cli.models.config import yaml
from nesso_cli.models.models import DBTProperties
import pytest

@pytest.fixture()
def dbt_properties(setup_source):
    dp = DBTProperties(file_path=setup_source)
    yield dp

def test_set_yaml_content(dbt_properties):
    dbt_properties[dbt_properties.resource_type] = "test"
    dbt_properties.set_yaml_content()

    with open(dbt_properties.file_path, "r") as file:
        yaml_dict = yaml.load(file)

    assert yaml_dict == {"version": 2, dbt_properties.resource_type: "test"}

def test_set_columns_order(TEST_TABLE_ACCOUNT, dbt_properties):
    def _get_columns_order(path):
        with open(path, "r") as file:
            yaml_dict = yaml.load(file)

        columns = yaml_dict[dbt_properties.resource_type][0]["tables"][0]["columns"]
        columns_order = [col["name"] for col in columns]

        return columns_order

    initial_columns_order = [
        "id",
        "name",
        "email",
        "mobile",
        "country",
        "_viadot_downloaded_at_utc",
    ]

    columns_order = _get_columns_order(dbt_properties.file_path)

    assert columns_order == initial_columns_order

    desired_columns_order = [
        "id",
        "mobile",
        "country",
        "name",
        "_viadot_downloaded_at_utc",
        "email",
    ]
    dbt_properties.set_columns_order(
        desired_order=desired_columns_order, table_name=TEST_TABLE_ACCOUNT
    )

    columns_order = _get_columns_order(dbt_properties.file_path)

    assert columns_order == desired_columns_order

def test_get_yaml_table_columns(TEST_TABLE_ACCOUNT, dbt_properties):
    columns_metadata = dbt_properties.get_yaml_table_columns(
        table_name=TEST_TABLE_ACCOUNT,
    )
    assert columns_metadata == YAML_SOURCE_COLUMNS_METADATA

def test_coherence_scan(create_accounts_table, TEST_SOURCE, TEST_TABLE_ACCOUNT, dbt_properties):
    diff, yaml_columns, db_columns = dbt_properties.coherence_scan(
        schema_name=TEST_SOURCE,
        table_name=TEST_TABLE_ACCOUNT,
    )
    assert not diff
    assert yaml_columns == YAML_SOURCE_COLUMNS_METADATA
    assert db_columns == YAML_SOURCE_COLUMNS

def test_add_column(TEST_TABLE_ACCOUNT, dbt_properties):
    dbt_properties.add_column(
        table_name=TEST_TABLE_ACCOUNT,
        column_name="new_column_name",
        index=6,
        data_type="CHARACTER VARYING(256)",
    )

    yaml_columns_metadata = dbt_properties.get_yaml_table_columns(
        table_name=TEST_TABLE_ACCOUNT
    )

    assert yaml_columns_metadata == COLUMNS_AFTER_INSERT

def test_delete_column(TEST_TABLE_ACCOUNT, dbt_properties):
    dbt_properties.delete_column(
        table_name=TEST_TABLE_ACCOUNT, column_name="_viadot_downloaded_at_utc"
    )
    yaml_columns_metadata = dbt_properties.get_yaml_table_columns(
        table_name=TEST_TABLE_ACCOUNT
    )

    assert yaml_columns_metadata == COLUMNS_AFTER_DELETE
