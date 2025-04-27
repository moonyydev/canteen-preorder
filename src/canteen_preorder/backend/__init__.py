import sqlite3
import json
import time
from argon2 import PasswordHasher
from typing import Optional
from canteen_preorder.common import Meal, Id, User, Cost, OrderItem, Order, Category

class PreorderBackend:
    def __init__(self, db_path: str = "canteen.db") -> None:
        self.db = sqlite3.connect(db_path)
        self.__prepare()
        
        self.hasher = PasswordHasher()
    
    def __prepare(self) -> None:
        cur = self.db.cursor()
        cur.execute("""
        create table if not exists users (
            id integer primary key autoincrement,
            name text not null,
            email text not null unique,
            password text not null,
            staff integer
        );
        """)

        cur.execute("""
        create table if not exists meals (
            id integer primary key autoincrement,
            name text not null unique,
            cost integer not null,
            category integer not null,
            stock integer not null,
            available integer not null
        );
        """)

        cur.execute("""
        create table if not exists orders (
            id integer primary key autoincrement,
            user integer not null,
            order_time integer not null,
            data text not null
        );
        """)

        self.db.commit()

    # USERS
    def login(self, email: str, password: str) -> Optional[User]:
        cur = self.db.cursor()
        res = cur.execute("select id, name, email, staff, password from users where email = ?")
        data = res.fetchone()
        if data is None:
            return None
        hash_correct = self.hasher.verify(data[4], password)
        self.db.commit()
        if not hash_correct:
            return None
        return self.__user(data[0:4])


    def __user(row: tuple[int, str, str, int]) -> User:
        return User(row[0], row[1], row[2], row[3] > 0)
    
    def get_user(self, user_id: Id) -> Optional[User]:
        cur = self.db.cursor()
        res = cur.execute("select id, name, email, staff from users where id = ?", user_id)
        self.db.commit()
        data = res.fetchone()
        if data is None:
            return None
        return self.__user(data)

    # Staff Only
    def get_users(self) -> list[User]:
        cur = self.db.cursor()
        res = cur.execute("select id, name, email, staff from users")
        self.db.commit()
        return [self.__user(user) for user in res.fetchall()]

    def create_user(self, name: str, email: str, password: str, staff: bool = False) -> User:
        cur = self.db.cursor()
        password_hash = self.hasher.hash(password)
        cur.execute("insert into users (name, email, password, staff) values (?, ?, ?, ?)", name, email, password_hash, staff if 1 else 0)
        res = cur.execute("select id from users where email = ?", email)
        user_id: int = res.fetchone()[0]
        self.db.commit()
        return self.get_user(user_id)
    
    # MEALS
    def __meal(self, row: tuple[int, str, int, int, int, int]) -> Meal:
        return Meal(row[0], row[1], row[2], Category(row[3]), row[4], row[5] > 0)

    def get_meals(self) -> list[Meal]:
        cur = self.db.cursor()
        res = cur.execute("select id, name, cost, category, stock from meals")
        self.db.commit()
        return [self.__meal(meal) for meal in res.fetchall()]

    def get_meal(self, meal_id: Id) -> Optional[Meal]:
        cur = self.db.cursor()
        res = cur.execute("select id, name, cost, category, stock, available from meals where id = ?", meal_id)
        self.db.commit()
        data = res.fetchone()
        if data is None:
            return None
        return self.__meal(data)

    # Staff Only
    def create_meal(self, name: str, cost: Cost, category: Category, stock: int, available: bool = True) -> Meal:
        cur = self.db.cursor()
        cur.execute("insert into meals (name, cost, category, stock, available) values (?, ?, ?, ?, ?)", name, cost, category.value, stock, available if 1 else 0)
        res = cur.execute("select id, name, cost, category, stock, available from meals where name = ?", name)
        self.db.commit()
        return self.__meal(res.fetchone())

    def update_meal_stock(self, meal_id: Id, stock: int) -> None:
        cur = self.db.cursor()
        cur.execute("update meals set stock = ? where id = ?", stock, meal_id)
        self.db.commit()

    def update_meal_cost(self, meal_id: Id, cost: Cost) -> None:
        cur = self.db.cursor()
        cur.execute("update meals set cost = ? where id = ?", cost, meal_id)
        self.db.commit()
    
    def update_meal_availability(self, meal_id: Id, available: bool = False) -> None:
        cur = self.db.cursor()
        cur.execute("update meals set availability = ? where id = ?", available if 1 else 0, meal_id)
        self.db.commit()

    # ORDERS
    def __order(self, row: tuple[int, int, int, str]) -> Order:
        items: list[OrderItem] = json.loads(row[3])
        return Order(row[0], row[1], row[2], items)

    def get_orders(self) -> list[Order]:
        cur = self.db.cursor()
        res = cur.execute("select id, user, order_time, data from orders")
        self.db.commit()
        return [self.__order(orders) for orders in res.fetchall()]
    
    def get_order(self, order_id: Id) -> Optional[Order]:
        cur = self.db.cursor()
        res = cur.execute("select id, user, order_time, data from orders where id = ?", order_id)
        self.db.commit()
        data = res.fetchone()
        if data is None:
            return None
        return self.__order(data)

    def create_order(self, user_id: Id, items: list[OrderItem]) -> Order:
        items_str = json.dumps(items)
        order_time = int(time.time())
        cur = self.db.cursor()
        res = cur.execute("insert into orders (user, order_time, data) values (?, ?, ?) returning id", user_id, order_time, items_str)
        self.db.commit()
        order_id: int = res.fetchone()[0]
        return self.__order((order_id, user_id, order_time, items_str))