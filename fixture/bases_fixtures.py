"""Fixtures for Core."""
from utils.logger import Logger
from utils.runner import Runner

import pytest


@pytest.fixture(scope="session")
def custom_args(pytestconfig):
    """Parse custom arguments."""
    incoming_args = {
        option: pytestconfig.getoption(option) for option in ["level", "log"]
    }
    return incoming_args


@pytest.fixture(scope="session", autouse=True)
def logger(custom_args):
    """Initialize log configuration."""
    return Logger(
        name="framework",
        level=custom_args.get("level"),
        path=custom_args.get("log"),
    ).logger


@pytest.fixture(scope="session", autouse=True)
def runner(custom_args, logger):
    """Initialize execution and callback pipeline when the execution end."""
    logger.info("Custom arguments: %s" % custom_args)
    custom_args.update({"logger": logger})
    run = Runner(**custom_args)
    yield run
    # TODO run.pipeline_callback()
