"""Shared fixtures for the test suite."""

from collections.abc import Iterator

import pytest
from flask.testing import FlaskClient

import server


@pytest.fixture(autouse=True)
def _reset_rate_limit_state() -> Iterator[None]:
    """Clear the in-memory rate limit log so tests don't leak state."""
    server._request_log.clear()
    yield
    server._request_log.clear()


@pytest.fixture
def client() -> Iterator[FlaskClient]:
    """Flask test client with testing mode enabled."""
    server.app.config["TESTING"] = True
    with server.app.test_client() as test_client:
        yield test_client
