import sqlite3
from argon2 import PasswordHasher
from canteen_preorder.common import Meal, Id, User, Cost, OrderItem, Order

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
    def login(self, email: str, password: str) -> User:
        pass

    def __user(row: tuple(int, str, str, int)) -> User:
        return User(row[0], row[1], row[2], row[3] > 0)
    
    def get_user(self, user_id: Id) -> User:
        cur = self.db.cursor()
        res = cur.execute("select id, name, email, staff from users where id = ?", user_id)
        cur.close()
        return self.__user(res.fetchone())

    # Staff Only
    def get_users(self) -> list[User]:
        cur = self.db.cursor()
        res = cur.execute("select id, name, email, staff from users")
        cur.close()
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