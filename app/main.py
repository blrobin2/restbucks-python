from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi_etag import Etag, add_exception_handler
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Restbucks",
    description="An API for taking orders in a coffee shop"
)
add_exception_handler(app)


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
    db_shots = [models.EspressoShot(name=shot.value)
                for shot in schemas.EspressoShotEnum]
    db_locations = [models.ConsumeLocation(
        name=location.value) for location in schemas.ConsumeLocationEnum]
    db_statuses = [models.OrderStatus(name=status.value)
                   for status in schemas.OrderStatusEnum]
    db_products = [models.Product(name=product.value)
                   for product in schemas.ProductEnum]
    db.add_all(db_milks)
    db.add_all(db_sizes)
    db.add_all(db_shots)
    db.add_all(db_locations)
    db.add_all(db_statuses)
    db.add_all(db_products)

    db.commit()
    return True


def order_etag(request: Request):
    db = SessionLocal()
    db_order = crud.get_order(db, request.path_params['order_id'])
    db.close()
    return f"order:{db_order.id}{db_order.updated_at}"


@app.post("/orders", response_model=schemas.Order, tags=["orders"])
def create_order(
    order: schemas.OrderCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    db_order = crud.create_order(db=db, order=order)
    client_host = request.client.host
    response.headers['Location'] = f"{client_host}/orders/{db_order.id}"
    return db_order


@app.get("/orders", response_model=List[schemas.Order], tags=["orders"])
def get_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_orders(db, skip=skip, limit=limit)


@app.get(
    "/orders/{order_id}",
    response_model=schemas.Order,
    tags=["orders"],
    dependencies=[Depends(Etag(order_etag))]
)
def get_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


@app.put("/orders/{order_id}", response_model=schemas.Order, tags=["orders"])
def update_order(
    order_id: int,
    order: schemas.OrderUpdate,
    db: Session = Depends(get_db)
):
    db_order = crud.update_order(db=db, order_id=order_id, order=order)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


@app.delete("/orders/{order_id}", status_code=204, tags=["orders"])
def archive_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    status = crud.archive_order(db, order_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Order not found")

    if status is False:
        raise HTTPException(status_code=405, detail="Order already served")

    return Response(status_code=204)
