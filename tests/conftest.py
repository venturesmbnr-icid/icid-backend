import pytest
from starlette.testclient import TestClient
from api.index import app


@pytest.fixture(scope="session")
def client():
    """
    Starlette TestClient wrapping the FastAPI app.
    Shared across the entire test session for speed.
    """
    with TestClient(app) as c:
        yield c
