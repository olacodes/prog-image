import pytest
from starlette.testclient import TestClient

from process_service.main import app


@pytest.fixture(scope="module")
def test_app():
    yield TestClient(app)
