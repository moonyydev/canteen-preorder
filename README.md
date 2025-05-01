# Canteen Preorder System

**[SPECIFICATION](docs/SPECIFICATION.md)**

# Backend

**[BACKEND API](docs/BACKEND_API.md)**

## Level 1: Storage

The backend is built using the [sqlite database](https://www.sqlite.org/) to store everything in four tables: [users](https://github.com/moonyydev/canteen-preorder/blob/d90c9725ee731aef05edbbc01b4953f6c9b88260/src/canteen_preorder/backend/__init__.py#L19-L24), [meals](https://github.com/moonyydev/canteen-preorder/blob/d90c9725ee731aef05edbbc01b4953f6c9b88260/src/canteen_preorder/backend/__init__.py#L29-L36), [orders](https://github.com/moonyydev/canteen-preorder/blob/d90c9725ee731aef05edbbc01b4953f6c9b88260/src/canteen_preorder/backend/__init__.py#L40-L44), [order_items](https://github.com/moonyydev/canteen-preorder/blob/d90c9725ee731aef05edbbc01b4953f6c9b88260/src/canteen_preorder/backend/__init__.py#L48-L56). Yet, only the first three (3) contain standalone objects. Order items has been added to replace the previous json-driven order item storage, with one that is queryable from the db.

Additionally, the backend also uses [Argon2](https://www.argon2.com/) (a winner of the Password Hashing Competition) for [hashing passwords](https://en.wikipedia.org/wiki/Cryptographic_hash_function#Password_verification), this is imperative for security reasons, as if the passwords were stored in plain text, a potential attaker could read them and gain unathorised access to staff and student accounts. The relevant code can be found [here](https://github.com/moonyydev/canteen-preorder/blob/d90c9725ee731aef05edbbc01b4953f6c9b88260/src/canteen_preorder/backend/__init__.py#L147-L150) (user creation) and [here](https://github.com/moonyydev/canteen-preorder/blob/d90c9725ee731aef05edbbc01b4953f6c9b88260/src/canteen_preorder/backend/__init__.py#L81-L85) (login).

The backend also utilises a double-decker structure (e.g \_\_internal\_\* functions), this allows for performing all database operations on one [transaction](en.wikipedia.org/wiki/Database_transaction). This is a major data-security concern as in case of a failure somewhere in the code, it can lead to either an un-commited transaction or data corruption. Thanks to this, any internal function can call other internal function, on one transaction, which will later be either commited or rolled back in case of an exception. Example of this functionality can be found [here](https://github.com/moonyydev/canteen-preorder/blob/d90c9725ee731aef05edbbc01b4953f6c9b88260/src/canteen_preorder/backend/__init__.py#L133-L144).

## Level 2: The API

The API of the backend was a major concern even prior to it being coded. One of my biggest goals in the design of the API was for it to be stable, fully explained, and didn't have any side-effects. Thus, the first iteration of the design doc was created, culiminated in the [full documentation of the API](docs/BACKEND_API.md). The API has strict static-typing, not allowing Python's inherent weakness that is its dynamic typing to cause failures down the line.

Furthermore, the backend has three exceptions (or errors) of its own: NotFoundError (in case when a **referenced** object is not found), ConstraintError (in case a predestined constraint is not met) and AlreadyExistsError (in case an object with one of the unique properties of the object you're trying to create already exists). It is supposed to only raise *them*, if it raises a different exception, that can be considered it straying from its spec, thus a failure of the program.

## Level 3: Testing

Concluding the backend's full documentation, it also has its own [extensive test suite](https://github.com/moonyydev/canteen-preorder/blob/d90c9725ee731aef05edbbc01b4953f6c9b88260/tests/test_backend.py) built with [pytest](https://docs.pytest.org/en/stable/) made to make sure the backend runs up to spec and will not stray from it, even in edge and erroneous cases. This test suite covers the correct running of the backend as well as the incorrect and makes sure it throws the right exceptions in the case anything fails. It also contains helping functions to simulate an already-running instance.

All of the tests in the suite (as of 21:36 01/05/2025):
```
test_backend_init - tests if the backend initalises correctly
test_backend_create_user - tests if a user is created correctly and their data is correct
test_backend_login_user - tests if a login happens correctly
test_backend_create_user_twice - tests if an AlreadyExistsError is thrown in case a user with the same email or name already exists
test_backend_wrong_login - tests if a None is returned when wrong login data is entered
test_backend_get_users - tests if the correct list of users is retrieved
test_backend_get_user - tests if the correct user data is retrieved
test_backend_get_nonexistant_user - tests if a None is returned when you try to get a user that doesn't exist
test_backend_create_meal - tests if a meal is created correctly and its data is correct
test_backend_create_meal_twice - tests if an AlreadyExistsError is thrown in case a meal with the same name already exists 
test_backend_get_meals - tests if the correct list of meals is retrieved
test_backend_get_meal - tests if the correct meal data is retrieved
test_backend_get_nonexistant_meal - tests if a None is returned when you try to get a meal that doesn't exist
test_backend_update_meal_cost - tests if a meal's cost is updated properly
test_backend_update_nonexistant_meal_cost - tests if a NotFoundError is thrown when you try to edit the cost of a meal that doesn't exist
test_backend_update_meal_cost_wrong - tests if a ConstraintError is thrown in case you try to set the cost of a meal to non-positive value
test_backend_update_meal_stock - tests if a meal's stock is updated properly
test_backend_update_nonexistant_meal_stock - tests if a NotFoundError is thrown when you try to edit the stock of a meal that doesn't exist
test_backend_update_meal_stock_wrong - tests if a ConstraintError is thrown in case you try to set the cost of a meal to negative value
test_backend_update_meal_availability - tests if a meal's availability is updated properly
test_backend_update_nonexistant_meal_availability - tests if a NotFoundError is thrown when you try to edit the avaiability of a meal that doesn't exist
test_backend_create_order - tests if an order is created correctly and its data is correct
test_backend_create_order_wrong_meal - tests if a NotFoundError is thrown in case you try to create an order with a meal that doesn't exist
test_backend_create_order_high_quantity - tests if a ConstraintError is thrown in case you try to create an order with a higher quantity of a meal than its stock
test_backend_get_orders - tests if the correct list of orders is retrieved
test_backend_get_order - tests if the correct order data is retrieved
test_backend_get_nonexistant_order - tests if a None is returned when you try to get an order that doesn't exist
test_backend_create_order_no_user - tests if a NotFoundError is thrown in case you try to create an order with a user that doesn't exist
test_backend_create_order_negative_quantity - tests if a ConstraintError is thrown if you try to create an order with a negative quantity of a meal
test_backend_create_order_zero_quantity - tests if a ConstraintError is thrown if you try to create an order with a zero quantity of a meal
test_backend_create_order_atomicity - tests if the database is corrupted in case any possible exceptions happen in the process of creating an order
test_backend_update_meal_atomicity - tests if the database is corrupted in case any possible exceptions happen in the process of creating a meal
test_backend_order_total - tests if the order's inline total is the same as the expected total
```