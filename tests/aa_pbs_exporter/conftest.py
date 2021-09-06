"""conftest.py file for aa_pbs_exporter"""
import json
import logging
from dataclasses import dataclass
from importlib import resources
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pytest

APP_LOG_LEVEL = logging.INFO
TEST_LOG_LEVEL = logging.DEBUG


@dataclass
class FileResource:
    file_path: Path
    data: Any


@pytest.fixture(scope="session", name="logger")
def _logger(test_log_path):
    """A central logger that will log to file."""
    # log_file_name = f"{__name__}.log"
    log_dir_path: Path = test_log_path / Path("test-logs")

    logger = configure_file_logger(
        log_dir=log_dir_path, logger_name=__name__, log_level=TEST_LOG_LEVEL
    )

    return logger


def configure_file_logger(
    log_dir: str, logger_name: str, log_level: Union[str, int]
) -> logging.Logger:
    """Configure a logger with a RotatingFileHandler.

    Note: Calling this function more than once with the same logger_name
    will result in duplicated logs.
    """
    log_file_name = f"{logger_name}.log"
    logger_ = logging.getLogger(logger_name)
    log_dir_path: Path = Path(log_dir)
    log_dir_path.mkdir(parents=True, exist_ok=True)
    log_file_path = log_dir_path / Path(log_file_name)
    handler = log_file_handler(log_file_path, log_level=int(log_level))
    logger_.addHandler(handler)
    logger_.setLevel(log_level)
    ############################################################
    # NOTE add file handler to other library modules as needed #
    ############################################################
    # async_logger = logging.getLogger("eve_esi_jobs")
    # async_logger.addHandler(file_handler)
    # async_logger.setLevel(log_level)
    logger_.info("Rotating File Logger initializd at %s", log_file_path)
    return logger_


def log_file_handler(
    file_path: Path,
    log_level: int = logging.WARNING,
    format_string: Optional[str] = None,
):
    handler = RotatingFileHandler(file_path, maxBytes=102400, backupCount=10)
    if format_string is None:
        format_string = (
            "%(asctime)s %(levelname)s:%(funcName)s: "
            "%(message)s [in %(pathname)s:%(lineno)d]"
        )
    handler.setFormatter(logging.Formatter(format_string))
    handler.setLevel(log_level)
    return handler


@pytest.fixture(scope="session", name="test_log_path")
def test_log_path_(test_app_data_dir):
    """Make a test-log directory under the app data directory"""
    log_path = test_app_data_dir / Path("test-logs")
    print(f"Logging at: {log_path}")
    return log_path


@pytest.fixture(scope="session", name="test_app_data_dir")
def test_app_data_dir_(tmp_path_factory):
    """make a temp directory for app data."""
    test_app_data_dir = tmp_path_factory.mktemp("aa_pbs_exporter-")
    return test_app_data_dir


@pytest.fixture(scope="session")
def example_resource(logger: logging.Logger) -> dict:
    """Load a resource file from a package directory.

    An example of loading a single resource file.
    """
    try:
        resource_path: str = "tests.aa_pbs_exporter.resources"
        resource_name: str = "example.json"
        with resources.open_text(resource_path, resource_name) as data_file:
            data = json.load(data_file)
            logger.info("Loaded resource file %s from %s", resource_name, resource_path)
            return data
    except Exception as ex:
        logger.exception(
            "Unable to load resource file %s from %s Error msg %s",
            resource_name,
            resource_path,
            ex,
        )
        raise ex


@pytest.fixture(scope="session", name="json_resources")
def json_resources_() -> Dict[str, FileResource]:
    """
    Load all resource files in a directory to a dict indexed by file name.

    Excludes __init__.py
    """
    resource_path: str = "tests.aa_pbs_exporter.json_resources"
    sample_data = make_file_resources_from_resource_path(resource_path)
    return sample_data


def make_file_resources_from_resource_path(
    resource_path,
    exclude_suffixes: Optional[List[str]] = None,
):
    file_paths = collect_resource_paths(resource_path, exclude_suffixes)
    file_resources = {}
    for file_path in file_paths:
        data = file_path.read_text()
        file_resource = FileResource(file_path=file_path, data=data)
        file_resources[file_path.name] = file_resource
    assert "__init__.py" not in file_resources
    return file_resources


def collect_resource_paths(
    resource_path: str,
    exclude_suffixes: Optional[List[str]] = None,
) -> List[Path]:
    """Returns a list of Paths in a resource directory, excluding the __init__.py"""
    if exclude_suffixes is None:
        exclude_suffixes = []
    result = []
    with resources.path(resource_path, "__init__.py") as data_path:
        for file in data_path.parent.glob("*.*"):
            if file.name != "__init__.py" and file.suffix not in exclude_suffixes:
                result.append(file)
    return result


@pytest.fixture(scope="session")
def pairing_package_pdf(logger) -> FileResource:
    resource_path = "tests.aa_pbs_exporter.resources"
    resource_name = "PBS_PHX_October_2021_20210905134803.pdf"
    return load_file_resource(
        resource_path=resource_path,
        resource_name=resource_name,
        logger=logger,
        path_only=True,
    )


def load_file_resource(
    resource_path: str,
    resource_name: str,
    logger: logging.Logger,
    path_only: bool = False,
    read_text: bool = True,
) -> FileResource:
    """
    Load a file resource.

    Load a string or bytes as a FileResource. Can optionaly return only a path to a
    file, with None as data.

    Args:
        resource_path ([type]): [description]
        resource_name ([type]): [description]
        logger ([type]): [description]
        path_only ([type], optional): [description]. Defaults to False.
        read_text ([type], optional): [description]. Defaults to True.

    Raises:
        ex: [description]

    Returns:
        FileResource: [description]
    """
    try:
        with resources.path(resource_path, resource_name) as data_path:
            data: Optional[Union[str, bytes]] = None
            if read_text:
                if not path_only:
                    data = data_path.read_text()
                    logger.debug(
                        "Loaded resource file %s from %s", resource_name, resource_path
                    )
                return FileResource(file_path=data_path, data=data)
            else:
                if not path_only:
                    data = data_path.read_bytes()
                    logger.debug(
                        "Loaded resource file %s from %s", resource_name, resource_path
                    )
                return FileResource(file_path=data_path, data=data)
    except Exception as ex:
        logger.exception(
            "Unable to load resource file %s from %s Error msg %s",
            resource_name,
            resource_path,
            ex,
        )
        raise ex


@pytest.fixture(autouse=True)
def env_setup(monkeypatch, test_app_data_dir):
    """environment variables set for each test."""
    monkeypatch.setenv(
        "pfmsoft_aa_pbs_exporter_TESTING",
        "True",
    )
    monkeypatch.setenv(
        "pfmsoft_aa_pbs_exporter_LOG_LEVEL",
        str(APP_LOG_LEVEL),
    )
    monkeypatch.setenv(
        "pfmsoft_aa_pbs_exporter_APP_DIR",
        str(test_app_data_dir),
    )
