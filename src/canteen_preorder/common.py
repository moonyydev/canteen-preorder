from typing import NamedTuple
from enum import Enum

type Id = int # the id of an object (in the database)
type Cost = int # 2-point fixed decimal cost, eg. 100 is 1.00, 451 is 4.51
type OrderItem = tuple[Id, int, Cost] # the id of a meal ordered, the quantity, and the cost a piece at the time of the order

class User(NamedTuple):
    user_id: Id
    name: str
    email: str
    staff: bool = False # whether or not the user is part of the staff

class Category(Enum):
    BREAKFAST = 0
    LUNCH = 1
    SNACK = 2

class Meal(NamedTuple):
    meal_id: Id
    name: str
    cost: Cost
    category: Category
    stock: int
    available: bool = True # wther it's available to buy, if this is false, a meal is  classified as discontinued

class Order(NamedTuple):
    order_id: Id
    user_id: Id
    order_time: int # the time the order happened at, as a unix timestamp
    items: list[OrderItem]