import os
import shutil
from pathlib import Path

import agate
import nesso_cli.models.context as context
import pytest
from conftest import TestData, test_tables_nrows
from nesso_cli.models.common import (
    call_shell,
    check_if_relation_exists,
    convert_list_of_options_to_dict,
    dict_diff,
    drop,
    execute_sql,
    get_current_dbt_profile,
    get_current_dbt_profiles_dir,
    get_current_dbt_project_obj,
    get_db_table_columns,
    get_dbt_target,
    get_local_schema,
    get_project_name,
    profile,
    run_dbt_operation,
    run_in_dbt_project,
)
from nesso_cli.models.config import config, yaml

PROJECT_NAME = "duckdb"
PROJECT_DIR = Path(__file__).parent.joinpath("dbt_projects", "duckdb")
context._set("PROJECT_DIR", PROJECT_DIR)


@pytest.fixture(scope="function")
def FAKE_DBT_PROFILES_DIR():
    profiles_dir = "/tmp/fake_project"

    shutil.rmtree(profiles_dir, ignore_errors=True)
    Path(profiles_dir).mkdir(parents=True, exist_ok=True)

    yield Path(profiles_dir)

    shutil.rmtree(profiles_dir, ignore_errors=True)


@pytest.fixture(scope="function")
def FAKE_DBT_PROFILES_PATH(FAKE_DBT_PROFILES_DIR):
    profiles_dir = FAKE_DBT_PROFILES_DIR.joinpath("profiles.yml")
    profiles_dir.unlink(missing_ok=True)

    yield profiles_dir

    profiles_dir.unlink(missing_ok=True)


def test_call_shell():
    command = "/usr/bin/ls"
    result = call_shell(command)
    files = result.split("\n")
    assert "dbt_project.yml" in files


def test_call_shell_with_args():
    command = "/usr/bin/ls"
    args = ["-a"]
    result = call_shell(command, args=args)
    files = result.split("\n")
    assert ".nesso" in files


def test_run_in_dbt_project():
    @run_in_dbt_project
    def check_if_in_dbt_project():
        cwd = os.getcwd()
        return str(cwd) == str(PROJECT_DIR)

    decorator_works = check_if_in_dbt_project()
    assert decorator_works


def test_get_project_name():
    test_project_dir = (
        Path(__file__).parent.absolute().joinpath("dbt_projects", "duckdb")
    )
    project = get_project_name(test_project_dir)

    test_project_dir_2 = (
        Path(__file__).parent.absolute().joinpath("dbt_projects", "postgres")
    )
    project_2 = get_project_name(test_project_dir_2)

    assert project == "duckdb"
    assert project_2 == "postgres"


def test_get_dbt_target(FAKE_DBT_PROFILES_DIR, FAKE_DBT_PROFILES_PATH):
    test_target = "test_target"
    fake_profiles = {PROJECT_NAME: {"target": test_target, "outputs": {}}}
    with open(FAKE_DBT_PROFILES_PATH, "w") as f:
        yaml.dump(fake_profiles, f)

    target = get_dbt_target(
        profiles_path=FAKE_DBT_PROFILES_PATH, project_name=PROJECT_NAME
    )
    assert target == test_target


def test_get_local_schema(FAKE_DBT_PROFILES_DIR, FAKE_DBT_PROFILES_PATH):
    test_target = "test_target"
    test_schema = "test_schema"
    fake_profiles = {
        PROJECT_NAME: {
            "target": test_target,
            "outputs": {test_target: {"schema": test_schema}},
        }
    }
    with open(FAKE_DBT_PROFILES_PATH, "w") as f:
        yaml.dump(fake_profiles, f)

    schema = get_local_schema(
        profiles_path=FAKE_DBT_PROFILES_PATH, project_name=PROJECT_NAME
    )
    assert schema == test_schema

    # Ensure 'prod' target is not supported.
    with pytest.raises(ValueError):
        get_local_schema(
            profiles_path=FAKE_DBT_PROFILES_PATH,
            project_name=PROJECT_NAME,
            target="prod",
        )


def test_get_current_dbt_profile():
    # Setup.
    working_dir = os.getcwd()

    postgres_project_dir = (
        Path(__file__).parent.absolute().joinpath("dbt_projects", "postgres")
    )
    trino_project_dir = (
        Path(__file__).parent.absolute().joinpath("dbt_projects", "trino")
    )

    # Test.
    os.chdir(postgres_project_dir)
    profile = get_current_dbt_profile()
    assert profile == "postgres"

    os.chdir(trino_project_dir)
    profile = get_current_dbt_profile()
    assert profile == "trino"

    # Cleanup.
    os.chdir(working_dir)


def test_get_current_dbt_profiles_dir():
    working_dir = os.getcwd()

    test_project_dir = (
        Path(__file__).parent.absolute().joinpath("dbt_projects", "duckdb")
    )
    os.chdir(test_project_dir)

    profiles_dir = get_current_dbt_profiles_dir()

    assert profiles_dir == test_project_dir

    # Cleanup.
    os.chdir(working_dir)


def test_get_db_table_columns(setup_source, create_accounts_table, TEST_SOURCE, TEST_TABLE_ACCOUNT):
    data = get_db_table_columns(table_name=TEST_TABLE_ACCOUNT, schema_name=TEST_SOURCE)
    assert data == {
        "id": "BIGINT",
        "name": "CHARACTER VARYING(256)",
        "email": "CHARACTER VARYING(256)",
        "mobile": "CHARACTER VARYING(256)",
        "country": "CHARACTER VARYING(256)",
        "_viadot_downloaded_at_utc": "TIMESTAMP WITH TIME ZONE",
    }


def test_get_current_dbt_project_obj():
    # Setup.
    working_dir = os.getcwd()

    test_project_dir = (
        Path(__file__).parent.absolute().joinpath("dbt_projects", "duckdb")
    )
    os.chdir(test_project_dir)
    context._set("DBT_PROJECT", None)

    # Test.
    project = get_current_dbt_project_obj()
    assert project.project_name == "duckdb"

    # Cleanup.
    os.chdir(working_dir)
    context._set("DBT_PROJECT", None)


def test_check_if_relation_exists():
    seed = "countries_example"
    schema = config.bronze_schema

    # Assumptions.
    assert not check_if_relation_exists(name=seed, schema=schema, target="prod")

    # Create table.
    dbt_project_obj = get_current_dbt_project_obj(target="prod")
    dbt_project_obj.seed(select=[seed], target="prod")

    # Validate.
    assert check_if_relation_exists(name=seed, schema=schema, target="prod")

    # Cleanup using dbt's drop function
    drop(name=seed, schema=schema, kind="table")


def test_execute_sql_fetches_data(create_contacts_table, TEST_TABLE_CONTACT):
    # Assumptions.
    schema = config.bronze_schema
    assert check_if_relation_exists(schema=schema, name=TEST_TABLE_CONTACT)

    # Test.
    sql = f"SELECT * FROM {schema}.{TEST_TABLE_CONTACT};"
    table = execute_sql(sql)
    assert isinstance(table, agate.Table)
    assert len(table.rows) == 100


def test_drop():
    # Set up.
    table_schema = config.bronze_schema
    table_name = "test_table"
    table_fqn = f"{table_schema}.{table_name}"
    view_schema = config.silver_schema
    view_name = "test_view"
    view_fqn = f"{view_schema}.{view_name}"

    execute_sql(f"CREATE TABLE IF NOT EXISTS {table_fqn} (id int);", commit=True, target="dev")
    execute_sql(f"CREATE SCHEMA IF NOT EXISTS {view_schema};", commit=True, target="dev")
    execute_sql(
        f"CREATE OR REPLACE VIEW {view_fqn} AS SELECT * FROM {table_fqn};",
        commit=True,
        target="dev",
    )

    # Assumptions.
    assert check_if_relation_exists(schema=table_schema, name=table_name)
    assert check_if_relation_exists(schema=view_schema, name=view_name)

    # Test.
    drop(name=view_name, schema=view_schema, kind="view")
    assert not check_if_relation_exists(schema=view_schema, name=view_name)

    drop(name=table_name, schema=table_schema, kind="table")
    assert not check_if_relation_exists(schema=table_schema, name=table_name)

    # Cleanup.
    execute_sql(f"DROP SCHEMA IF EXISTS {view_schema} CASCADE;", commit=True)


@pytest.mark.parametrize(
    "options, expected_dict",
    [
        (["--key1", "val1", "--key2", "val2"], {"key1": "val1", "key2": "val2"}),
        (["--key1", "value-2", "--key2", "val2"], {"key1": "value-2", "key2": "val2"}),
        ([], {}),
    ],
)
def test_convert_list_of_options_to_dict(options, expected_dict):
    data = convert_list_of_options_to_dict(options)
    assert data == expected_dict


@pytest.mark.parametrize(
    "options",
    [
        ["--key1", "val1", "--key2"],
        ["key1", "val1", "--key2"],
        ["--key1", "val1", "--key2", "--value2"],
        ["key1", "--val1", "key2", "--value2"],
    ],
)
def test_convert_list_of_options_to_dict_handles_incorrect_input(options):
    with pytest.raises(ValueError):
        convert_list_of_options_to_dict(options)


def test_profile(setup_model):
    info = profile(TestData.model.name)
    assert info["nrows"] == test_tables_nrows
    assert info["size"] == "0 MB"


def test_dict_diff_equal():
    """Verify that dict_diff() returns correct diff for equal dictionaries."""
    dict1 = {"a": 1, "b": 2, "c": 3}
    dict2 = dict1
    diff = dict_diff(dict1, dict2)
    assert diff == {}


def test_dict_diff_different():
    """Verify that dict_diff() returns correct diff for different dictionaries."""
    dict1 = {"a": 1, "b": 2, "c": 3}
    dict2 = {"a": 1, "b": 2, "c": 4}
    diff = dict_diff(dict1, dict2)
    assert diff == {"c": 4}


def test_run_dbt_operation_without_args():
    """Test running a macro without arguments."""
    output = run_dbt_operation("test_args_macro", quiet=True)

    assert "arg1=None" in output
    assert "arg2=None" in output
    assert "arg3=None" in output


def test_run_dbt_operation_with_args():
    """Test running a macro with arguments."""
    args = {
        "arg1": "value1",
        "arg2": "value2",
        "arg3": "value3",
    }

    output = run_dbt_operation("test_args_macro", args=args, quiet=True)

    # Check that the macro received the arguments
    assert "arg1=value1" in output
    assert "arg2=value2" in output
    assert "arg3=value3" in output
