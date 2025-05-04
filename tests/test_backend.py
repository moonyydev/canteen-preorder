import pytest
from canteen_preorder.backend import PreorderBackend, ConstraintError, NotFoundError, AlreadyExistsError
from canteen_preorder.common import Category, Meal, User, Order

def testing_backend() -> PreorderBackend:
    return PreorderBackend(":memory:")

def test_backend_init():
    testing_backend()

def test_backend_create_user():
    backend = testing_backend()
    u1 = backend.create_user("test_user", "test_user@gmail.com", "test123pass", True)
    u1e = User(u1.user_id, "test_user", "test_user@gmail.com", True)
    assert u1 == u1e
    u2 = backend.create_user("user2", "2nduser@gmail.com", "somepassword", False)
    u2e = User(u2.user_id, "user2", "2nduser@gmail.com", False)
    assert u2 == u2e

def user_testing_collection(backend: PreorderBackend) -> list[User]:
    users: list[User] = []
    users.append(backend.create_user("test_user", "test_user@gmail.com", "test123pass", True))
    users.append(backend.create_user("user2", "2nduser@gmail.com", "somepassword", False))
    users.append(backend.create_user("userthree", "userthethird@gmail.com", "wowpass", False))
    users.append(backend.create_user("userV", "fifthuser@gmail.com", "unexpectedpassword", False))
    return users

def test_backend_login_user():
    backend = testing_backend()
    user1 = user_testing_collection(backend)[0]
    user2 = backend.login("test_user@gmail.com", "test123pass")
    assert user1 == user2

def test_backend_create_user_twice():
    backend = testing_backend()
    backend.create_user("test_user", "test_user@gmail.com", "test123pass", True)
    with pytest.raises(AlreadyExistsError):
        backend.create_user("test_user", "test_user@gmail.com", "differentpass", False)

def test_backend_wrong_login():
    backend = testing_backend()
    user_testing_collection(backend)
    assert backend.login("thisemaildoesntexist@gmail.com", "nordoesthispassword") is None
    assert backend.login("userthethird@gmail.com", "nordoesthispassword") is None
    assert backend.login("thisemaildoesntexisteither@gmail.com", "test123pass") is None

def test_backend_get_users():
    backend = testing_backend()
    users = user_testing_collection(backend)
    assert users == backend.get_users()

def test_backend_get_user():
    backend = testing_backend()
    user1 = user_testing_collection(backend)[1]
    user2 = backend.get_user(user1.user_id)
    assert user1 == user2

def test_backend_get_nonexistant_user():
    backend = testing_backend()
    user_testing_collection(backend)
    assert backend.get_user(11) is None

def meal_testing_collection(backend: PreorderBackend) -> list[Meal]:
    meals: list[Meal] = []
    meals.append(backend.create_meal("Fruit Salad", 820, Category.SNACK, 2))
    meals.append(backend.create_meal("Turkey Sandwich", 650, Category.LUNCH, 5))
    meals.append(backend.create_meal("Chicken Sandwich", 670, Category.LUNCH, 1))
    meals.append(backend.create_meal("Vegeterian Sandwich", 710, Category.LUNCH, 8))
    return meals

def test_backend_create_meal():
    backend = testing_backend()
    m1 = backend.create_meal("Fruit Salad", 820, Category.SNACK, 2)
    m1e = Meal(m1.meal_id, "Fruit Salad", 820, Category.SNACK, 2)
    assert m1 == m1e
    m2 = backend.create_meal("Chicken Sandwich", 670, Category.LUNCH, 1)
    m2e = Meal(m2.meal_id, "Chicken Sandwich", 670, Category.LUNCH, 1)
    assert m2 == m2e

def test_backend_create_meal_twice():
    backend = testing_backend()
    backend.create_meal("Fruit Salad", 820, Category.SNACK, 2)
    with pytest.raises(AlreadyExistsError):
        backend.create_meal("Fruit Salad", 810, Category.LUNCH, 3)

def test_backend_get_meals():
    backend = testing_backend()
    meals = meal_testing_collection(backend)
    assert meals == backend.get_meals(True)

def test_backend_get_meal():
    backend = testing_backend()
    meal1 = meal_testing_collection(backend)[2]
    meal2 = backend.get_meal(meal1.meal_id)
    assert meal1 == meal2

def test_backend_get_nonexistant_meal():
    backend = testing_backend()
    meal_testing_collection(backend)
    assert backend.get_meal(83) is None

def test_backend_update_meal_cost():
    backend = testing_backend()
    target = meal_testing_collection(backend)[1]
    backend.update_meal_cost(target.meal_id, target.cost + 30)
    expected = Meal(target.meal_id, target.name, target.cost + 30, target.category, target.stock, target.available)
    assert expected == backend.get_meal(target.meal_id)

def test_backend_update_nonexistant_meal_cost():
    backend = testing_backend()
    meal_testing_collection(backend)
    with pytest.raises(NotFoundError):
        backend.update_meal_cost(98, 210)

def test_backend_update_meal_cost_wrong():
    backend = testing_backend()
    meal_testing_collection(backend)
    with pytest.raises(ConstraintError):
        backend.update_meal_cost(1, 0)
    
    with pytest.raises(ConstraintError):
        backend.update_meal_cost(1, -350)


def test_backend_update_meal_stock():
    backend = testing_backend()
    target = meal_testing_collection(backend)[1]
    backend.update_meal_stock(target.meal_id, 7)
    expected = Meal(target.meal_id, target.name, target.cost, target.category, 7, target.available)
    assert expected == backend.get_meal(target.meal_id)

def test_backend_update_nonexistant_meal_stock():
    backend = testing_backend()
    meal_testing_collection(backend)
    with pytest.raises(NotFoundError):
        backend.update_meal_stock(37, 4)

def test_backend_update_meal_stock_wrong():
    backend = testing_backend()
    meal_testing_collection(backend)
    with pytest.raises(ConstraintError):
        backend.update_meal_stock(1, -35)


def test_backend_update_meal_availability():
    backend = testing_backend()
    target = meal_testing_collection(backend)[1]
    backend.update_meal_availability(target.meal_id, False)
    expected = Meal(target.meal_id, target.name, target.cost, target.category, target.stock, False)
    assert expected == backend.get_meal(target.meal_id)

def test_backend_update_nonexistant_meal_availability():
    backend = testing_backend()
    meal_testing_collection(backend)
    with pytest.raises(NotFoundError):
        backend.update_meal_availability(15, False)

def order_testing_collection(backend: PreorderBackend) -> list[Order]:
    users = [user.user_id for user in backend.get_users()]
    orders: list[Order] = []
    orders.append(backend.create_order(users[len(orders) % len(users)], [(1, 1), (2, 2)]))
    orders.append(backend.create_order(users[len(orders) % len(users)], [(2, 2), (4, 3)]))
    orders.append(backend.create_order(users[len(orders) % len(users)], [(3, 1), (1, 1)]))
    orders.append(backend.create_order(users[len(orders) % len(users)], [(4, 3), (4, 2)]))
    return orders

def test_backend_create_order():
    backend = testing_backend()
    user_testing_collection(backend)
    meal_testing_collection(backend)
    o1 = backend.create_order(3, [(1, 1), (4, 2)])
    expected_order = Order(1, 3, o1.order_time,  [(1, 1, 820), (4, 2, 710)])
    assert o1 == expected_order
    o2 = backend.get_order(1)
    assert o2 == expected_order
    o3 = backend.get_orders()[0]
    assert o3 == expected_order

def test_backend_create_order_wrong_meal():
    backend = testing_backend()
    user_testing_collection(backend)
    with pytest.raises(NotFoundError):
        backend.create_order(1, [(1, 1), (3, 1), (82, 3), (2, 1)])

def test_backend_create_order_high_quantity():
    backend = testing_backend()
    user_testing_collection(backend)
    meal_testing_collection(backend)
    with pytest.raises(ConstraintError):
        backend.create_order(1, [(1, 1), (4, 1), (3, 15), (2, 1)])

def test_backend_get_orders():
    backend = testing_backend()
    user_testing_collection(backend)
    meal_testing_collection(backend)
    orders = order_testing_collection(backend)
    assert orders == backend.get_orders(True)

def test_backend_get_order():
    backend = testing_backend()
    user_testing_collection(backend)
    meal_testing_collection(backend)
    order1 = order_testing_collection(backend)[1]
    order2 = backend.get_order(order1.order_id)
    assert order1 == order2

def test_backend_get_nonexistant_order():
    backend = testing_backend()
    user_testing_collection(backend)
    meal_testing_collection(backend)
    order_testing_collection(backend)
    assert backend.get_order(33) is None

def test_backend_create_order_no_user():
    backend = testing_backend()
    meal_testing_collection(backend)
    with pytest.raises(NotFoundError):
        backend.create_order(13, [(1, 2), (2, 1)])

def test_backend_create_order_negative_quantity():
    backend = testing_backend()
    meal_testing_collection(backend)
    user_testing_collection(backend)
    with pytest.raises(ConstraintError):
        backend.create_order(1, [(1, -3)])

def test_backend_create_order_zero_quantity():
    backend = testing_backend()
    meal_testing_collection(backend)
    user_testing_collection(backend)
    with pytest.raises(ConstraintError):
        backend.create_order(1, [(1, 0)])

def test_backend_create_order_atomicity():
    backend = testing_backend()
    meals_expected = meal_testing_collection(backend)
    user_testing_collection(backend)

    with pytest.raises(ConstraintError):
        backend.create_order(2, [(1, 1), (3, 82)])
    assert backend.get_meals(True) == meals_expected

    with pytest.raises(NotFoundError):
        backend.create_order(18, [(1, 1), (3, 1)])
    assert backend.get_meals(True) == meals_expected

    with pytest.raises(ConstraintError):
        backend.create_order(1, [(3, -2), (1, -15)])
    assert backend.get_meals(True) == meals_expected

def test_backend_update_meal_atomicity():
    backend = testing_backend()
    meals_expected = meal_testing_collection(backend)

    with pytest.raises(NotFoundError):
        backend.update_meal_cost(8, 310)
    assert meals_expected == backend.get_meals(True)

    with pytest.raises(NotFoundError):
        backend.update_meal_stock(9, 3)
    assert meals_expected == backend.get_meals(True)
    
    with pytest.raises(NotFoundError):
        backend.update_meal_availability(9)
    assert meals_expected == backend.get_meals(True)

    with pytest.raises(ConstraintError):
        backend.update_meal_cost(1, -50)
    assert meals_expected == backend.get_meals(True)

    with pytest.raises(ConstraintError):
        backend.update_meal_cost(2, 0)
    assert meals_expected == backend.get_meals(True)

    with pytest.raises(ConstraintError):
        backend.update_meal_stock(1, -9)
    assert meals_expected == backend.get_meals(True)

def test_backend_order_total():
    backend = testing_backend()
    meals = meal_testing_collection(backend)
    users = user_testing_collection(backend)
    total = meals[0].cost + meals[1].cost * 3 + meals[3].cost * 2
    order = backend.create_order(users[0].user_id, [(meals[0].meal_id, 1), (meals[1].meal_id, 3), (meals[3].meal_id, 2)])
    costs = [item[2] * item[1] for item in order.items]
    assert sum(costs) == total