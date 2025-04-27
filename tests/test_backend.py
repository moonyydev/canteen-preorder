import pytest
from sqlite3 import DatabaseError
from canteen_preorder.backend import PreorderBackend

def test_backend_init():
    PreorderBackend(":memory:")

def test_backend_create_user():
    backend = PreorderBackend(":memory:")
    user1 = backend.create_user("test_user", "test_user@gmail.com", "test123pass", True)
    user2 = backend.login("test_user@gmail.com", "test123pass")
    assert user1 == user2