from typing import List

from pprint import pprint
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Obviously, don't do this in real life
@app.post("/seed")
def seed_database(db: Session = Depends(get_db)):
    db_milks = [models.Milk(name=milk.value) for milk in schemas.MilkEnum]
    db_sizes = [models.Size(name=size.value) for size in schemas.SizeEnum]
    db_shots = [models.EspressoShot(name=shot.value) for shot in schemas.EspressoShotEnum]
    db_locations = [models.ConsumeLocation(name=location.value) for location in schemas.ConsumeLocationEnum]
    db_statuses = [models.OrderStatus(name=status.value) for status in schemas.OrderStatusEnum]
    db_products = [models.Product(name=product.value) for product in schemas.ProductEnum]
    db.add_all(db_milks)
    db.add_all(db_sizes)
    db.add_all(db_shots)
    db.add_all(db_locations)
    db.add_all(db_statuses)
    db.add_all(db_products)

    db.commit()
    return True

@app.post("/orders", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = crud.create_order(db=db, order=order)
    pprint(db_order)
    return db_order


@app.get("/orders", response_model=List[schemas.Order])
def get_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_orders(db, skip=skip, limit=limit)


@app.get("/orders/{order_id}", response_model=schemas.Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order
