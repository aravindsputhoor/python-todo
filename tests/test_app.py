import pytest
# Adjust this import to match where your Flask 'app' instance is created:
# e.g., from app import app, from run import app, etc.
from run import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_route(client):
    """Test that the home page loads successfully."""
    response = client.get("/")
    assert response.status_code == 200


def test_get_todos(client):
    """Test fetching the todo list."""
    response = client.get("/todos")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_create_todo(client):
    """Test creating a new todo item."""
    payload = {"title": "Test task from Pytest"}
    response = client.post("/todos", json=payload)
    assert response.status_code in [200, 201]