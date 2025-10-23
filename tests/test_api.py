
import pytest

# https://pytest-with-eric.com/pytest-advanced/pytest-fastapi-testing/

def test_api(mock_client):
    response = mock_client.get("/")
    assert response is not None
    assert response.status_code == 200
    assert response.json() == {"message": "python-fastapi-openapi.yml k8s"}
    