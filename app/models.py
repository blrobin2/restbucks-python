from typing import TYPE_CHECKING
from sqlalchemy import Column, ForeignKey, DateTime, Integer, String, func
if TYPE_CHECKING:
    hybrid_property = property
else:
    from sqlalchemy.ext.hybrid import hybrid_property

from sqlalchemy.orm import relationship

import datetime
import locale

from .database import Base


class Milk(Base):
    __tablename__ = "milks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    def __repr__(self):
        return f"{self.name}"


class Size(Base):
    __tablename__ = "sizes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    def __repr__(self):
        return f"{self.name}"


class EspressoShot(Base):
    __tablename__ = "espresso_shots"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    def __repr__(self):
        return f"{self.name}"


class ConsumeLocation(Base):
    __tablename__ = "consume_locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    def __repr__(self):
        return f"{self.name}"


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    def __repr__(self):
        return f"{self.name}"


class OrderStatus(Base):
    __tablename__ = "order_statuses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    def __repr__(self):
        return f"{self.name}"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    total = Column(Integer)
    location_id = Column(Integer, ForeignKey("consume_locations.id"))
    status_id = Column(Integer, ForeignKey("order_statuses.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=datetime.datetime.now
    )

    location = relationship("ConsumeLocation", lazy="joined")
    status = relationship("OrderStatus", lazy="joined")
    items = relationship(
        "OrderItem",
        back_populates="order",
        lazy="joined",
        uselist=True
    )

    def __repr__(self):
        return (
            f"Order(id={self.id!r}, location={self.location!r}, "
            "status={self.status!r}, items={self.items!r})"
        )

    @hybrid_property
    def total_cost(self):
        return locale.currency(self.total / 100)

    @total_cost.expression
    def total_cost(cls):
        return func.concat('$', cls.total / 100)

    @total_cost.setter
    def total_cost(self, value):
        self.total = value * 100

    def can_delete(self) -> bool:
        current_status = self.status.name
        return current_status not in ['served', 'collected', 'cancelled']


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    quantity = Column(Integer, nullable=False, default=1)
    product_id = Column(Integer, ForeignKey("products.id"))
    milk_id = Column(Integer, ForeignKey("milks.id"))
    size_id = Column(Integer, ForeignKey("sizes.id"))
    espresso_shot_id = Column(Integer, ForeignKey("espresso_shots.id"))

    order = relationship("Order", back_populates="items", lazy="joined")
    product = relationship("Product", lazy="joined")
    milk = relationship("Milk", lazy="joined")
    size = relationship("Size", lazy="joined")
    espresso_shot = relationship("EspressoShot", lazy="joined")

    def __repr__(self):
        return (
            f"OrderItem(id={self.id!r}, product={self.product!r}, "
            "milk={self.milk!r}, size={self.size!r}, "
            "shot={self.espresso_shot!r})"
        )
