"""Module for managing global context variables."""

from typing import Any

from nesso_cli.models.common import get_current_dbt_project_path


project_path = get_current_dbt_project_path()
ctx = {
    "PROJECT_DIR": project_path,
    "DBT_PROJECT": None,
    "PROJECT_NAME": project_path.name,
}


def _set(key: str, value: Any) -> None:  # noqa: ANN401
    global context  # noqa: PLW0602
    ctx.update({key: value})


def get(key: str) -> Any:  # noqa: ANN401
    """Get a context variable value."""
    global context  # noqa: PLW0602
    return ctx.get(key)
