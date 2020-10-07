"""Fixtures for Application."""
from bases.application import Application

import pytest

defaultargs = {"auto_start": True, "auto_close": True}


@pytest.fixture(scope="module")
def app_instance(custom_args):
    """Single application instance to be reused by all fixtures."""
    runtime_args = defaultargs.copy()
    runtime_args.update(custom_args)
    return Application(**runtime_args)


@pytest.fixture(scope="function")
def app(app_instance):
    """Provide application instance object to run tests."""
    app_instance.setup()

    yield app_instance

    app_instance.teardown()