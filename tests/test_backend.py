import pytest
from sqlite3 import DatabaseError
from canteen_preorder.backend import PreorderBackend

def test_backend_init():
    PreorderBackend(":memory:")

def test_backend_create_and_login_user():
    backend = PreorderBackend(":memory:")
    user1 = backend.create_user("test_user", "test_user@gmail.com", "test123pass", True)
    user2 = backend.login("test_user@gmail.com", "test123pass")
    assert user1 == user2

def test_backend_create_and_login_multi_user():
    backend = PreorderBackend(":memory:")
    backend.create_user("test_user", "test_user@gmail.com", "test123pass", True)
    backend.create_user("user2", "2nduser@gmail.com", "somepassword", False)
    user1 = backend.create_user("userthree", "userthethird@gmail.com", "wowpass", False)
    backend.create_user("userV", "fifthuser@gmail.com", "unexpectedpassword", False)
    user2 = backend.login("userthethird@gmail.com", "wowpass")
    assert user1 == user2