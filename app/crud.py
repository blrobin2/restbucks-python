from sqlalchemy.orm import Session

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


def create_order(db: Session, order: schemas.OrderCreate):
    db_order_items = [
        order_item_schema_to_order_item(db, item)
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


def order_item_schema_to_order_item(
    db: Session,
    order_item: schemas.OrderItemCreate
):
    return models.OrderItem(
        product=get_product_by_name(db, order_item.product_name),
        size=get_size_by_name(db, order_item.size),
        milk=get_milk_by_name(db, order_item.milk),
        espresso_shot=get_espresso_shot_by_name(db, order_item.shot),
        quantity=order_item.quantity
    )
