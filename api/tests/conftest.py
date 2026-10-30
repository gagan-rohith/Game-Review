import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client():
    # The context manager runs the app's lifespan (Redis client setup and teardown).
    with TestClient(app) as c:
        yield c
