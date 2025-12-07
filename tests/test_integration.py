import pytest
from app import create_app
from extensions import db
from models import User, Task
from datetime import date


@pytest.fixture
def app():
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        WTF_CSRF_ENABLED=False,
        SECRET_KEY="test",
    )

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def register_and_login(client):
    client.post(
        "/register", data={"username": "test", "password": "pw", "confirm": "pw"}
    )
    client.post("/login", data={"username": "test", "password": "pw"})


def test_user_registration(client, app):
    resp = client.post(
        "/register",
        data={
            "username": "alice",
            "password": "secret",
            "confirm": "secret",
        },
        follow_redirects=True,
    )

    assert b"Registration successful" in resp.data


def test_login_flow(client):
    register_and_login(client)
    resp = client.get("/")
    assert resp.status_code == 200


def test_task_creation(client, app):
    register_and_login(client)

    resp = client.post(
        "/tasks/new",
        data={"title": "My Task", "description": "hello", "due_date": "2024-01-01"},
        follow_redirects=True,
    )

    assert b"Task created" in resp.data

    with app.app_context():
        assert Task.query.count() == 1
