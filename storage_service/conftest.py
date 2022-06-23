import pytest
from starlette.testclient import TestClient

from storage_service.app.main import app


@pytest.fixture(scope="module")
def test_app():
    yield TestClient(app)
