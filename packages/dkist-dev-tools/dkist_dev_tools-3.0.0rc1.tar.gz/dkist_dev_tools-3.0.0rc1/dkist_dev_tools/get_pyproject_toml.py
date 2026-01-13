"""Functions for getting default pyproject TOMLs."""

import sys
from pathlib import Path

from dkist_dev_tools.console import console

PYPROJECT_NAME = "pyproject.toml"
SCIENCE_TOWNCRIER_NAME = "towncrier_science.toml"


def get_pyproject_toml(
    project_dir: Path | str, toml_name: str = PYPROJECT_NAME, fail_if_missing: bool = True
) -> Path:
    """Load a pyproject.toml file from a given directory."""
    if isinstance(project_dir, str):
        project_dir = Path(project_dir)

    project_dir = project_dir.resolve()
    pyproject_file = project_dir / toml_name

    if fail_if_missing and not pyproject_file.exists():
        console.log(
            f"[red]Could not find '{toml_name}' file in '{project_dir}' :wilted_flower:[/red]"
        )
        sys.exit(1)

    return pyproject_file
