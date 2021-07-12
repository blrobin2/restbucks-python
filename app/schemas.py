from enum import Enum
from pydantic import BaseModel
from typing import List, Optional


class MilkEnum(str, Enum):
    none = 'none'
    skim = 'skim'
    semi = 'semi'
    whole = 'whole'


class Milk(BaseModel):
    id: int
    name: MilkEnum

    class Config:
        orm_mode = True


class SizeEnum(str, Enum):
    small = 'small'
    medium = 'medium'
    large = 'large'


class Size(BaseModel):
    id: int
    name: SizeEnum

    class Config:
        orm_mode = True


class EspressoShotEnum(str, Enum):
    none = 'none'
    single = 'single'
    double = 'double'
    triple = 'triple'


class EspressoShot(BaseModel):
    id: int
    name: EspressoShotEnum

    class Config:
        orm_mode = True


class ConsumeLocationEnum(str, Enum):
    take_away = 'take away'
    in_shop = 'in shop'


class ConsumeLocation(BaseModel):
    id: int
    name: ConsumeLocationEnum

    class Config:
        orm_mode = True


class OrderStatusEnum(str, Enum):
    pending = 'pending'
    paid = 'paid'
    served = 'served'
    collected = 'collected'


class OrderStatus(BaseModel):
    id: int
    name: OrderStatusEnum

    class Config:
        orm_mode = True


class ProductEnum(str, Enum):
    latte = 'latte'
    cappuccino = 'cappuccino'
    espresso = 'espresso'
    tea = 'tea'


class Product(BaseModel):
    id: int
    name: ProductEnum

    class Config:
        orm_mode = True


class OrderItemBase(BaseModel):
    quantity: int = 1


class OrderItemCreate(OrderItemBase):
    product_name: ProductEnum
    size: SizeEnum
    milk: MilkEnum = MilkEnum.none
    shot: EspressoShotEnum = EspressoShotEnum.none


class OrderItem(OrderItemBase):
    id :int
    product: Product
    size: Size
    milk: Milk
    espresso_shot: EspressoShot

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    pass


class OrderCreate(OrderBase):
    location: ConsumeLocationEnum
    items: List[OrderItemCreate]
    status: Optional[OrderStatusEnum] = OrderStatusEnum.pending


class Order(OrderBase):
    id: int
    location: ConsumeLocation
    items: List[OrderItem] = []
    status: Optional[OrderStatus]
    total: Optional[int]

    class Config:
        orm_mode = True
