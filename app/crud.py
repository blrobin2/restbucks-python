import datetime
from sqlalchemy.orm import Session
from typing import Union

from . import models, schemas


def get_product_by_name(db: Session, product: str):
    return db.query(models.Product)\
        .filter(models.Product.name == product).first()


def get_milk_by_name(db: Session, milk: str):
    return db.query(models.Milk).filter(models.Milk.name == milk).first()


def get_size_by_name(db: Session, size: str):
    return db.query(models.Size).filter(models.Size.name == size).first()


def get_espresso_shot_by_name(db: Session, shot: str):
    return db.query(models.EspressoShot)\
        .filter(models.EspressoShot.name == shot).first()


def get_consume_location_by_name(db: Session, location: str):
    return db.query(models.ConsumeLocation)\
        .filter(models.ConsumeLocation.name == location).first()


def get_order_status_by_name(db: Session, status: str):
    return db.query(models.OrderStatus)\
        .filter(models.OrderStatus.name == status).first()


def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()


def get_order_item(db: Session, order_item_id: int):
    return db.query(models.OrderItem)\
        .filter(models.OrderItem.id == order_item_id).first()


def create_order(db: Session, order: schemas.OrderCreate):
    db_order_items = [
        order_item_create_schema_to_order_item(db, item)
        for item
        in order.items
    ]
    location = get_consume_location_by_name(db, order.location)
    status = get_order_status_by_name(db, order.status)
    db_order = models.Order(
        location=location,
        status=status,
        items=db_order_items
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def update_order(db: Session, order_id: int, order: schemas.OrderUpdate):
    db_order = get_order(db, order_id)
    if not db_order:
        return None

    db_order_items = [
        order_item_update_schema_to_order_item(db, item)
        for item
        in order.items
    ]
    location = get_consume_location_by_name(db, order.location)
    status = get_order_status_by_name(db, order.status)
    db_order.location = location
    db_order.status = status
    db_order.items = db_order_items
    db_order.updated_at = datetime.datetime.now()
    db.commit()
    db.refresh(db_order)
    return db_order


def archive_order(db: Session, order_id: int):
    db_order = get_order(db, order_id)
    if not db_order:
        return None

    if not db_order.can_delete():
        return False

    cancel_status = get_order_status_by_name(db, 'cancelled')
    db_order.status = cancel_status
    db.commit()
    return True


def order_item_create_schema_to_order_item(
    db: Session,
    order_item: schemas.OrderItemCreate
):
    order_items_elements = get_shared_order_item_elements(db, order_item)
    return models.OrderItem(
        product=order_items_elements['product'],
        size=order_items_elements['size'],
        milk=order_items_elements['milk'],
        espresso_shot=order_items_elements['espresso_shot'],
        quantity=order_item.quantity
    )


def order_item_update_schema_to_order_item(
    db: Session,
    order_item: schemas.OrderItemUpdate
):
    db_order_item = get_order_item(db, order_item.id)
    if not db_order_item:
        return order_item_create_schema_to_order_item(db, order_item)

    order_items_elements = get_shared_order_item_elements(db, order_item)
    db_order_item.product = order_items_elements['product']
    db_order_item.size = order_items_elements['size']
    db_order_item.milk = order_items_elements['milk']
    db_order_item.espresso_shot = order_items_elements['espresso_shot']
    db_order_item.quantity = order_item.quantity
    return db_order_item


def get_shared_order_item_elements(
    db: Session,
    order_item: Union[schemas.OrderItemCreate, schemas.OrderItemUpdate]
):
    return dict(
        product=get_product_by_name(db, order_item.product_name),
        size=get_size_by_name(db, order_item.size),
        milk=get_milk_by_name(db, order_item.milk),
        espresso_shot=get_espresso_shot_by_name(db, order_item.shot),
    )
