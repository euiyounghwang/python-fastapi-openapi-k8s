
import pytest
from fastapi.testclient import TestClient
from main import app
from injector import logger

# https://pytest-with-eric.com/pytest-advanced/pytest-fastapi-testing/


@pytest.mark.skip(reason="This test is currently under development and not ready.")
def test_feature_in_progress():
    assert False # This assertion will not be reached


def test_api(mock_client):
    # response = mock_client.get("/")
    client = TestClient(app)
    response = client.get("/")
    assert response is not None
    assert response.status_code == 200
    assert response.json() == {"message": "python-fastapi-openapi.yml k8s"}
    

test_data = [(i, {'message': 'Hello World [{}]'.format(i)}) for i in [2, 0]]
@pytest.mark.parametrize("input_value, expected_output", test_data)
def test_some_api_parameterized(input_value, expected_output):
    client = TestClient(app)
    response = client.get(f"/test/{input_value}")
    assert response.status_code == 200
    assert response.json() == expected_output