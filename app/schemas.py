from enum import Enum
from pydantic import BaseModel
from typing import List, Optional


class Milk(str, Enum):
    none = 'none'
    skim = 'skim'
    semi = 'semi'
    whoe = 'whole'


class Size(str, Enum):
    small = 'small'
    medium = 'medium'
    large = 'large'


class EspressoShot(str, Enum):
    none = 'none'
    single = 'single'
    double = 'double'
    triple = 'triple'


class ConsumeLocation(str, Enum):
    take_away = 'take away'
    in_shop = 'in shop'


class OrderStatus(str, Enum):
    pending = 'pending'
    paid = 'paid'
    served = 'served'
    collected = 'collected'


class OrderItemBase(BaseModel):
    product_name: str
    quantity: int = 1
    size: Size
    milk: Milk = Milk.none
    shot: EspressoShot = EspressoShot.none


class OrderItemCreate(OrderItemBase):
    pass


class OrderItem(OrderItemBase):
    id :int

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    location: ConsumeLocation


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class Order(OrderBase):
    id: int
    items: List[OrderItem] = []
    status: Optional[OrderStatus]
    cost: Optional[int]

    class Config:
        orm_model =True

