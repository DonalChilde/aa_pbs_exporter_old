"""These tests are not meant to be run during normal testing.

This is a convenience to regenerate dynamic test data on demand.
Set REFRESH_RESOURCES to True and run tests to generate data.
"""

import json
from pathlib import Path

import yaml

REFRESH_RESOURCES = False


def test_example_resources():
    if not REFRESH_RESOURCES:
        assert True
        return
    resource_data = [{"color": "blue"}, {"color": "red"}]
    resource_parent_path = Path(__file__).parent

    # json resources
    resource_subpath = resource_parent_path / "json_resources"
    resource_subpath.mkdir(parents=True, exist_ok=True)
    init = resource_subpath / Path("__init__.py")
    init.touch()
    data_file = resource_subpath / Path("data.json")
    data_file.write_text(json.dumps(resource_data, indent=2))

    # yaml resources
    resource_subpath = resource_parent_path / "yaml_resources"
    resource_subpath.mkdir(parents=True, exist_ok=True)
    init = resource_subpath / Path("__init__.py")
    init.touch()
    data_file = resource_subpath / Path("data.yaml")
    data_file.write_text(yaml.safe_dump(resource_data, indent=2))
