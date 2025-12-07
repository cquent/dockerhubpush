import pytest
from app import _build_postgres_uri
from models import User, Task
from datetime import date


def test_build_postgres_uri_env(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://example.com/db")
    assert _build_postgres_uri() == "postgresql://example.com/db"


def test_user_password_hashing():
    u = User(username="testuser")
    u.set_password("mypassword")
    assert u.check_password("mypassword") is True
    assert u.check_password("wrongpass") is False


def test_task_default_completed():
    t = Task(title="Test Task")
    assert t.is_completed is False
