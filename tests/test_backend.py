from canteen_preorder.backend import PreorderBackend
from canteen_preorder.common import Category, Meal, User

def testing_backend() -> PreorderBackend:
    return PreorderBackend(":memory:")

def test_backend_init():
    testing_backend()

def user_testing_collection(backend: PreorderBackend) -> list[User]:
    users = []
    users.append(backend.create_user("test_user", "test_user@gmail.com", "test123pass", True))
    users.append(backend.create_user("user2", "2nduser@gmail.com", "somepassword", False))
    users.append(backend.create_user("userthree", "userthethird@gmail.com", "wowpass", False))
    users.append(backend.create_user("userV", "fifthuser@gmail.com", "unexpectedpassword", False))
    return users

def test_backend_create_and_login_user():
    backend = testing_backend()
    user1 = user_testing_collection(backend)[0]
    user2 = backend.login("test_user@gmail.com", "test123pass")
    assert user1 == user2

def test_backend_create_and_get_users():
    backend = testing_backend()
    users = user_testing_collection(backend)
    assert users == backend.get_users()

def test_backend_get_user():
    backend = testing_backend()
    user1 = user_testing_collection(backend)[1]
    user2 = backend.get_user(user1.user_id)
    assert user1 == user2

def meal_testing_collection(backend: PreorderBackend) -> list[Meal]:
    meals = []
    meals.append(backend.create_meal("Fruit Salad", 820, Category.SNACK, 2))
    meals.append(backend.create_meal("Turkey Sandwich", 650, Category.LUNCH, 5))
    meals.append(backend.create_meal("Chicken Sandwich", 670, Category.LUNCH, 1))
    meals.append(backend.create_meal("Vegeterian Sandwich", 710, Category.LUNCH, 8))
    return meals

def test_backend_create_meal():
    backend = testing_backend()
    meal_testing_collection(backend)
    
def test_backend_get_meals():
    backend = testing_backend()
    meals = meal_testing_collection(backend)
    assert meals == backend.get_meals()

def test_backend_get_meal():
    backend = testing_backend()
    meal1 = meal_testing_collection(backend)[2]
    meal2 = backend.get_meal(meal1.meal_id)
    assert meal1 == meal2