import pytest
from app import create_app
from app.models import db


@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }
    app = create_app(config_class=test_config)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200


def test_get_todos(client):
    response = client.get("/todos")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_create_todo(client):
    payload = {"title": "Test task"}
    response = client.post("/todos", json=payload)
    assert response.status_code in [200, 201]