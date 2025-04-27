import pytest
from sqlite3 import DatabaseError
from canteen_preorder.backend import PreorderBackend

def test_backend_init():
    PreorderBackend(":memory:")