# USERS

    def login(self, email: str, password: str) -> Optional[User]
login user with email `email` and password `password`,

this function returns a `None` if the user doesn't exist or passwords don't match

    def get_user(self, user_id: Id) -> Optional[User]
get user with id `user_id`,

this function returns a `None` if there's no user with id `user_id`

## Staff Only
    def get_users(self) -> list[User]
get all the users

    def create_user(self, name: str, email: str, password: str, staff: bool = False) -> User
create user with name `name`, email `email`, password `password` and the staff attribute `staff`,

this function raises `sqlite3.IntegrityError` if the user already exists

# MEALS
    def get_meals(self) -> list[Meal]
get all meals in the database

    def get_meal(self, meal_id: Id) -> Optional[Meal]
get meal with id `meal_id`,

this function returns a `None` if there's no meal with id `meal_id`

## Staff Only
    def create_meal(self, name: str, cost: Cost, category: Category, stock: int, available: bool = True) -> Meal
create meal with name `name`, cost `cost`, category `category`, stock `stock`, and availability attribute `available`,

this function raises an `sqlite3.IntegrityError` if the meal already exists

    def update_meal_stock(self, meal_id: Id, stock: int) -> None
update the stock field of a meal with id `meal_id` to `stock`,

this function raises `BackendNotFoundException` if there's no meal with id `meal_id`

    def update_meal_cost(self, meal_id: Id, cost: Cost) -> None
update the cost field of a meal with id `meal_id` to `cost`,

this function raises `BackendNotFoundException` if there's no meal with id `meal_id`

    def update_meal_availability(self, meal_id: Id, available: bool = False) -> None
update the availability attribute of a meal with id `meal_id` to `available`,

this function raises `BackendNotFoundException` if there's no meal with id `meal_id`

# ORDERS
    def create_order(self, user_id: Id, items: list[OrderItem]) -> Order
create order with user id `user_id`, items `items`, current time as timestamp,

this function raises `BackendNotFoundException` if any of the meals in the order items aren't found,

this function raises `BackendConstraintException` if the order exceeds the available stock

## Staff Only
    def get_orders(self) -> list[Order]
get all the orders

    def get_order(self, order_id: Id) -> Optional[Order]
get order with id `order_id`,

this function returns a `None` if there's no order with id `order_id`
