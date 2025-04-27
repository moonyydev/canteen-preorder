import pytest
from sqlite3 import DatabaseError
from canteen_preorder.backend import PreorderBackend
from canteen_preorder.common import Category

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

def test_backend_create_and_get_users():
    backend = PreorderBackend(":memory:")
    users = []
    users.append(backend.create_user("test_user", "test_user@gmail.com", "test123pass", True))
    users.append(backend.create_user("user2", "2nduser@gmail.com", "somepassword", False))
    users.append(backend.create_user("userthree", "userthethird@gmail.com", "wowpass", False))
    users.append(backend.create_user("userV", "fifthuser@gmail.com", "unexpectedpassword", False))
    assert users == backend.get_users()

def test_backend_get_user():
    backend = PreorderBackend(":memory:")
    backend.create_user("test_user", "test_user@gmail.com", "test123pass", True)
    user1 = backend.create_user("user2", "2nduser@gmail.com", "somepassword", False)
    backend.create_user("userthree", "userthethird@gmail.com", "wowpass", False)
    backend.create_user("userV", "fifthuser@gmail.com", "unexpectedpassword", False)
    user2 = backend.get_user(user1.user_id)
    assert user1 == user2


def test_backend_create_meal():
    backend = PreorderBackend(":memory:")
    backend.create_meal("Fruit Salad", 820, Category.SNACK, 2)
    backend.create_meal("Turkey Sandwich", 650, Category.LUNCH, 5)
    backend.create_meal("Chicken Sandwich", 670, Category.LUNCH, 1)
    backend.create_meal("Vegeterian Sandwich", 710, Category.LUNCH, 8)
