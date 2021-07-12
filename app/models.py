from sqlalchemy import Column, ForeignKey, Integer, String, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

import locale

from .database import Base


class Milk(Base):
    __tablename__ = "milks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)


class Size(Base):
    __tablename__ = "sizes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)


class EspressoShot(Base):
    __tablename__ = "espresso_shots"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(unique=True, index=True, nullable=False)


class ConsumeLocation(Base):
    __tablename__ = "consume_locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(unique=True, index=True, nullable=False)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(unique=True, index=True, nullable=False)


class OrderStatus(Base):
    __tablename__ = "order_statuses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(unique=True, index=True, nullable=False)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    total = Column(Integer, nullable=False)
    location_id = Column(Integer, ForeignKey("consume_locations.id"))
    status_id = Column(Integer, ForeignKey("order_statuses.id"))
    currency_id = Column(Integer, ForeignKey("currencies.id"))

    location = relationship("ConsumeLocation")
    status = relationship("OrderStatus")
    items = relationship("OrderItem", back_populates="order")

    @hybrid_property
    def total_cost(self):
        return locale.currency(self.total / 100)


    @total_cost.expression
    def total_cost(cls):
        return func.concat('$', cls.total / 100)


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, nullable=False, default=1)
    product_id = Column(Integer, ForeignKey("products.id"))
    milk_id = Column(Integer, ForeignKey("milks.id"))
    size_id = Column(Integer, ForeignKey("sizes.id"))
    espresso_shot_id = Column(Integer, ForeignKey("espresso_shots.id"))

    order = relationship("Order", back_populates="items")
    milk = relationship("Milk")
    size = relationship("Size")
    espresso_shot = relationship("EspressoShot")
