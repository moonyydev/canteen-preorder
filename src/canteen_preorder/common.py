from typing import NamedTuple
from enum import Enum

type Id = int
type Cost = int
type OrderItem = tuple(Id, int)

class User(NamedTuple):
    user_id: Id
    name: str
    email: str
    staff: bool = False

class Meal(NamedTuple):
    meal_id: Id
    name: str
    cost: Cost
    category: int
    stock: int
    available: bool = True

class Category(Enum):
    BREAKFAST = 0
    LUNCH = 1
    SNACK = 2

class Order(NamedTuple):
    order_id: Id
    user_id: Id
    order_time: int
    items: list[OrderItem]