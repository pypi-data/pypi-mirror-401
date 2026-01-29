from pathlib import Path
from unittest.mock import Mock

from conftest import TestData
from typer.testing import CliRunner

from nesso_cli.models import context
from nesso_cli.models.config import yaml
from nesso_cli.models.main import app
from nesso_cli.models.model import bootstrap_yaml


PROJECT_DIR = Path(__file__).parent.joinpath("dbt_projects", "duckdb")
context._set("PROJECT_DIR", PROJECT_DIR)
TEST_DBT_TARGET = "dev"

runner = CliRunner()


def test_model_bootstrap(MODEL, MODEL_PATH, MART):
    # Assumptions.
    assert not MODEL_PATH.exists()

    # Test.
    result = runner.invoke(app, ["model", "bootstrap", MODEL, "--subdir", MART])

    assert result.exit_code == 0
    assert MODEL_PATH.exists()

    # Cleaning up after the test
    MODEL_PATH.unlink()


def test_model_bootstrap_yaml(
    setup_model,
    MODEL,
    MODEL_YAML_PATH,
):
    # Delete model YAML file created by the `setup_model()` fixture.
    setup_model.unlink()

    # Assumption.
    assert not MODEL_YAML_PATH.exists()

    mock_ctx = Mock()
    mock_ctx.args = []

    bootstrap_yaml(
        ctx=mock_ctx,
        model=MODEL,
        env=TEST_DBT_TARGET,
    )

    assert MODEL_YAML_PATH.exists()
    assert setup_model.exists()

    expected_schema = TestData.model_props_no_overrides

    with open(setup_model) as f:
        schema = yaml.load(f)

    assert schema == expected_schema

    with open(setup_model) as f:
        yaml_str = f.read()

    assert "# data_tests:" in yaml_str


def test_model_bootstrap_yaml_provide_meta_as_options(
    setup_model,
    MODEL,
    MODEL_YAML_PATH,
):
    # Delete model YAML file created by the `setup_model()` fixture.
    setup_model.unlink()

    # Assumption.
    assert not MODEL_YAML_PATH.exists()

    mock_ctx = Mock()
    mock_ctx.args = ['--domains', '["model_domain"]']

    bootstrap_yaml(
        ctx=mock_ctx,
        model=MODEL,
        env=TEST_DBT_TARGET,
    )

    assert MODEL_YAML_PATH.exists()
    assert setup_model.exists()

    with open(setup_model) as f:
        schema = yaml.load(f)

    # Validate whether the `domain` key was created as expected, ie. the provided value
    # was added to the inherited list.
    assert schema == TestData.model_props_without_tests

    with open(setup_model) as f:
        yaml_str = f.read()

    assert "# data_tests:" in yaml_str
