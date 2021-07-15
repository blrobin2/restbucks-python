from fastapi import Request

from .database import SessionLocal
from . import crud


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def orders_etag(_request: Request):
    db = SessionLocal()
    db_order = crud.get_most_recent_order(db)
    db.close()
    return f"orders:{db_order.updated_at}"


def order_etag(request: Request):
    db = SessionLocal()
    db_order = crud.get_order(db, request.path_params['order_id'])
    db.close()
    return f"order:{db_order.id}:{db_order.updated_at}"
