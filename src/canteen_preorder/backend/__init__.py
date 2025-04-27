import sqlite3
from canteen_preorder.common import Meal, Id, User, Cost, OrderItem, Order

class PreorderBackend:
    def __init__(self, db_path: str = "canteen.db") -> None:
        self.db = sqlite3.connect(db_path)
        self.__prepare()
    
    def __prepare(self) -> None:
        cur = self.db.cursor()
        cur.execute("""
        create table if not exists users (
            id int primary key,
            name text not null,
            email text not null unique,
            password text not null,
            staff int
        );
        """)

        cur.execute("""
        create table if not exists meals (
            id int primary key,
            name text not null unique,
            cost int not null,
            category int not null,
            stock int not null,
            available int not null
        );
        """)

        cur.execute("""
        create table if not exists orders (
            id int primary key,
            user int not null,
            order_time int not null,
            data text not null
        );
        """)

        self.db.commit()

    # USERS
    def login(self, email: str, password: str) -> User:
        pass
    
    def get_user(self, user_id: Id) -> User:
        pass

    # Staff Only
    def create_user(self, name: str, email: str, password: str, staff: bool = False) -> User:
        pass
    
    # MEALS
    def get_meals(self) -> list[Meal]:
        pass

    def get_meal(self, meal_id: Id) -> Meal:
        pass

    # Staff Only
    def create_meal(self, name: str, cost: Cost, category: int, stock: int, available: bool = True) -> Meal:
        pass

    def update_meal_stock(self, meal_id: Id, stock: int) -> None:
        pass

    def update_meal_cost(self, meal_id: Id, cost: Cost) -> None:
        pass
    
    def update_meal_availability(self, meal_id: Id, available: bool = False) -> None:
        pass

    # ORDERS
    def get_orders(self) -> list[Order]:
        pass
    
    def get_order(self, order_id: Id) -> Order:
        pass

    def create_order(self, user_id: Id, items: list[OrderItem]) -> Order:
        pass