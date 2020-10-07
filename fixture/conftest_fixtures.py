from assertpy import soft_assertions

from fixture.application_fixtures import app  # noqa: F401
from fixture.application_fixtures import app_instance  # noqa: F401
from fixture.bases_fixtures import custom_args  # noqa: F401
from fixture.bases_fixtures import logger  # noqa: F401
from fixture.bases_fixtures import runner  # noqa: F401

import pytest


@pytest.fixture(scope="function", autouse=True)
def soft_assertion_wrapper():
    """Allow to run tests even with multiple assertion failures."""
    with soft_assertions():
        yield


def pytest_addoption(parser):
    """Allow to run the marked tests with specific command line options."""
    parser.addoption(
        "--log",
        action="store",
        default="framework.log",
        help="Specify a log file with a either full or relative path."
        "Usage: --log=log-example.log",
    )

    parser.addoption(
        "--level",
        action="store",
        default="info",
        help="Specify the logging level (debug|info|warning|error|critical)."
        "Usage: --level=debug",
    )
