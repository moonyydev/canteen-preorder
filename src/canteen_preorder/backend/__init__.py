import sqlite3
from sqlite3 import Cursor
import json
import time
from argon2 import PasswordHasher
import argon2
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
        # open transaction
        cur = self.db.cursor()
        user = self.__internal_login(cur, email, password)
        # commit transaction, function is read only, thus, safe
        self.db.commit()
        return user
        

    def __internal_login(self, cur: Cursor, email: str, password: str) -> Optional[User]:
        # find the user by email
        # password last so it can be excluded later by a simple splice index
        res = cur.execute("select id, name, email, staff, password from users where email = ?", (email, ))
        # get ONE result from the result set
        data = res.fetchone()
        # if user isn't found, return None
        if data is None:
            return None
        # verify may return a mismatch exception if the password is wrong
        try:
            # compared the stored hash with the password
            self.hasher.verify(data[4], password)
        except argon2.exceptions.VerifyMismatchError:
            return None
        # assemble User object
        return self.__user(data[0:4])


    def __user(self, row: tuple[int, str, str, int]) -> User:
        # row is (id, name, email, staff (1 if true, 0 if false))
        return User(row[0], row[1], row[2], row[3] > 0)
    
    def get_user(self, user_id: Id) -> Optional[User]:
        # open transaction
        cur = self.db.cursor()
        user = self.__internal_get_user(cur, user_id)
        # commit transaction, function is read only, thus, safe
        self.db.commit()
        return user
        

    def __internal_get_user(self, cur: Cursor, user_id: Id) -> Optional[User]:
        # get the user data with specified id
        res = cur.execute("select id, name, email, staff from users where id = ?", (user_id, ))
        # get ONE result from the result set
        data = res.fetchone()
        # if we didn't get any data, the user doesn't exist, return None
        if data is None:
            return None
        # assemble User object
        return self.__user(data)

    # Staff Only
    def get_users(self) -> list[User]:
        # open transaction
        cur = self.db.cursor()
        users = self.__internal_get_users(cur)
        # commit transaction, function is read only, thus, safe
        self.db.commit()
        return users

        
    def __internal_get_users(self, cur: Cursor) -> list[User]:
        # get all users
        res = cur.execute("select id, name, email, staff from users")
        # fetch ALL of the results
        data = res.fetchall()
        # go through all of the users in data, and assemble them into User objects
        return [self.__user(user) for user in data]

    def create_user(self, name: str, email: str, password: str, staff: bool = False) -> User:
        # open transaction
        cur = self.db.cursor()
        try:
            user = self.__internal_create_user(cur, name, email, password, staff)
        except Exception as e:
            # internal errored, rollback current transaction so the db doesn't get corrupted
            self.db.rollback()
            raise e
        else: 
            # the function ran correctly, commit transaction
            self.db.commit()
            return user
        
    def __internal_create_user(self, cur: Cursor, name: str, email: str, password: str, staff: bool = False) -> User:
        # create hash from the password passed in in the arguments
        # we hash the password so that you cannot just check the user's password in the database
        # because it's unsafe
        password_hash = self.hasher.hash(password)
        try:
            # insert the user into users, and return said user row data
            res = cur.execute("insert into users (name, email, password, staff) values (?, ?, ?, ?) returning id, name, email, staff", (name, email, password_hash, staff if 1 else 0))
        except sqlite3.IntegrityError:
            raise AlreadyExistsError("user with this name or email already exists")
        # fetch ONE results from the result set
        data = res.fetchone()
        # assemble into User object
        return self.__user(data)

    # MEALS
    def __meal(self, row: tuple[int, str, int, int, int, int]) -> Meal:
        # row is (id, name, cost, category, stock, available (1 if True, 0 if False))
        return Meal(row[0], row[1], row[2], Category(row[3]), row[4], row[5] > 0)

    def get_meals(self) -> list[Meal]:
        # open transaction
        cur = self.db.cursor()
        meals = self.__internal_get_meals(cur)
        # commit transaction, function is read only, thus, safe
        self.db.commit()
        return meals

        
    def __internal_get_meals(self, cur: Cursor) -> list[Meal]:
        # get all meals
        res = cur.execute("select * from meals")
        # fetch ALL results in the result set
        data = res.fetchall()
        # go through all of the meals in data, and assemble them into Meal objects
        return [self.__meal(meal) for meal in data]

    def get_meal(self, meal_id: Id) -> Optional[Meal]:
        # open transaction
        cur = self.db.cursor()
        meal = self.__internal_get_meal(cur, meal_id)
        # commit transaction, function is read only, thus, safe
        self.db.commit()
        return meal
        
    def __internal_get_meal(self, cur: Cursor, meal_id: Id) -> Optional[Meal]:
        # get the data of a meal that has id meal_id
        res = cur.execute("select * from meals where id = ?", (meal_id, ))
        # fetch ONE result from the result set
        data = res.fetchone()
        # if we didn't get any data, there's no meal matching the id, so return None
        if data is None:
            return None
        # assemble Meal object
        return self.__meal(data)

    # Staff Only
    def create_meal(self, name: str, cost: Cost, category: Category, stock: int, available: bool = True) -> Meal:
        # open transaction
        cur = self.db.cursor()
        try:
            meal = self.__internal_create_meal(cur, name, cost, category, stock, available)
        except Exception as e:
            # internal errored, rollback current transaction so the db doesn't get corrupted
            self.db.rollback()
            raise e
        else:
            # the function ran correctly, commit transaction
            self.db.commit()
            return meal

    def __internal_create_meal(self, cur: Cursor, name: str, cost: Cost, category: Category, stock: int, available: bool = True) -> Meal:
        try:
            # insert into meals, returning said meal's data
            res = cur.execute("insert into meals (name, cost, category, stock, available) values (?, ?, ?, ?, ?) returning *", (name, cost, category.value, stock, available if 1 else 0))
        except sqlite3.IntegrityError:
            raise AlreadyExistsError("meal with this name already exists in the database")
        # fetch ONE result from the result set
        data = res.fetchone()
        # assemble Meal object
        return self.__meal(data)

    def update_meal_stock(self, meal_id: Id, stock: int) -> None:
        # open transaction
        cur = self.db.cursor()
        try:
            self.__internal_update_meal_stock(cur, meal_id, stock)
        except Exception as e:
            # internal errored, rollback current transaction so the db doesn't get corrupted
            self.db.rollback()
            raise e
        else:
            # the function ran correctly, commit transaction
            self.db.commit()
    
    def __internal_update_meal_stock(self, cur: Cursor, meal_id: Id, stock: int) -> None:
        if stock < 0:
            raise ConstraintError("stock needs to be positive")
        # update stock in a row of meals of which the id is meal_id
        cur.execute("update meals set stock = ? where id = ?", (stock, meal_id))
        # if no rows have been changed, no meal has been modified, so there's no meal with meal_id
        if cur.rowcount == 0:
            raise NotFoundError("meal does not exist")

    def update_meal_cost(self, meal_id: Id, cost: Cost) -> None:
        # open transaction
        cur = self.db.cursor()
        try:
            self.__internal_update_meal_cost(cur, meal_id, cost)
        except Exception as e:
            # internal errored, rollback current transaction so the db doesn't get corrupted
            self.db.rollback()
            raise e
        else:
            # the function ran correctly, commit transaction
            self.db.commit()
    
    def __internal_update_meal_cost(self, cur: Cursor, meal_id: Id, cost: Cost) -> None:
        if cost <= 0:
            raise ConstraintError("cost needs to be positive")
        # update cost in a row of meals of which the id is meal_id
        cur.execute("update meals set cost = ? where id = ?", (cost, meal_id))
        # if no rows have been changed, no meal has been modified, so there's no meal with meal_id
        if cur.rowcount == 0:
            raise NotFoundError("meal does not exist")
    
    def update_meal_availability(self, meal_id: Id, available: bool = False) -> None:
        # open transaction
        cur = self.db.cursor()
        try:
            self.__internal_update_meal_availability(cur, meal_id, available)
        except Exception as e:
            # internal errored, rollback current transaction so the db doesn't get corrupted
            self.db.rollback()
            raise e
        else:
            # the function ran correctly, commit transaction
            self.db.commit()

    def __internal_update_meal_availability(self, cur: Cursor, meal_id: Id, available: bool = False) -> None:
        # update available in a row of meals of which the id is meal_id
        cur.execute("update meals set available = ? where id = ?", (available if 1 else 0, meal_id))
        # if no rows have been changed, no meal has been modified, so there's no meal with meal_id
        if cur.rowcount == 0:
            raise NotFoundError("meal does not exist")

    # ORDERS
    def __order(self, row: tuple[int, int, int, str]) -> Order:
        # row is (id, ordering user, order time, [(mmeal_id, quantity)] as json)
        items: list[OrderItem] = json.loads(row[3])
        return Order(row[0], row[1], row[2], items)

    def get_orders(self) -> list[Order]:
        # open transaction
        cur = self.db.cursor()
        orders = self.__internal_get_orders(cur)
        # commit transaction, function is read only, thus, safe
        self.db.commit()
        return orders
        
    def __internal_get_orders(self, cur: Cursor) -> list[Order]:
        # get all orders
        res = cur.execute("select * from orders")
        # fetch all the results from the result set
        data = res.fetchall()
        # go through the all of the orders in data and assemble them into Order objects
        return [self.__order(orders) for orders in data]
    
    def get_order(self, order_id: Id) -> Optional[Order]:
        # open transaction
        cur = self.db.cursor()
        order = self.__internal_get_order(cur, order_id)
        # commit transaction, function is read only, thus, safe
        self.db.commit()
        return order
        
    def __internal_get_order(self, cur: Cursor, order_id: Id) -> Optional[Order]:
        # get order with id order_id
        res = cur.execute("select * from orders where id = ?", (order_id, ))
        # fetch ONE result from the result set
        data = res.fetchone()
        # if we didn't get any data, there's no order matching the id, return None
        if data is None:
            return None
        # assemble Order object
        return self.__order(data)

    def create_order(self, user_id: Id, items: list[OrderItem]) -> Order:
        # open transaction
        cur = self.db.cursor()
        try:
            order = self.__internal_create_order(cur, user_id, items)
        except Exception as e:
            # internal errored, rollback current transaction so the db doesn't get corrupted
            self.db.rollback()
            raise e
        else:
            # the function ran correctly, commit transaction
            self.db.commit()
            return order
        

    def __internal_create_order(self, cur: Cursor, user_id: Id, items: list[OrderItem]) -> Order:
        # check if the user exists
        if self.__internal_get_user(cur, user_id) is None:
            raise NotFoundError("user does not exist")
        # turn items into a string with json
        items_str = json.dumps(items)
        # get current unix timestamp
        order_time = int(time.time())
        # insert order, returning the order's id
        res = cur.execute("insert into orders (user, order_time, data) values (?, ?, ?) returning id", (user_id, order_time, items_str))
        # fetch one result from the result set and get the 1st field
        order_id: int = res.fetchone()[0]
        # go through all items and deduct the order quantity from the stock
        for (item, quantity) in items:
            # if quantity is not positive, raise constraint exception
            if quantity <= 0:
                raise ConstraintError("quantity must be positive")
            # get meal with id of the item
            meal = self.__internal_get_meal(cur, item)
            # if there's no meal with that id, raise not found exception
            if meal is None:
                raise NotFoundError("meal does not exist")
            # if the stock is smaller than the quantity, raise constraint exception
            if meal.stock < quantity:
                raise ConstraintError("less stock than order quantity")
            # update the meal's stock
            self.__internal_update_meal_stock(cur, meal.meal_id, meal.stock - quantity)
        # assemble Order object
        return self.__order((order_id, user_id, order_time, items_str))

class NotFoundError(Exception):
    pass

class ConstraintError(Exception):
    pass

class AlreadyExistsError(Exception):
    pass