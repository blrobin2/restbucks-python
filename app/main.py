from fastapi import Depends, FastAPI
from fastapi_etag import add_exception_handler
from sqlalchemy.orm import Session

from . import models, schemas, deps
from .database import engine
from .routers import orders

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Restbucks",
    description="An API for taking orders in a coffee shop"
)
add_exception_handler(app)
app.include_router(orders.router)


# Obviously, don't do this in real life
@app.post("/seed")
def seed_database(db: Session = Depends(deps.get_db)):
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
