from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi_etag import Etag
from sqlalchemy.orm import Session

from .. import crud, schemas, deps


router = APIRouter()


@router.post("/orders", response_model=schemas.Order, tags=["orders"])
def create_order(
    order: schemas.OrderCreate,
    request: Request,
    response: Response,
    db: Session = Depends(deps.get_db)
):
    db_order = crud.create_order(db=db, order=order)
    client_host = request.client.host
    response.headers['Location'] = f"{client_host}/orders/{db_order.id}"
    return db_order


@router.get(
    "/orders",
    response_model=List[schemas.Order],
    dependencies=[Depends(Etag(deps.orders_etag))],
    tags=["orders"],
    responses={
        '304': dict(description='Not Modified: Cache hit, ETag not expired')
    }
)
def get_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)
):
    return crud.get_orders(db, skip=skip, limit=limit)


@router.get(
    "/orders/{order_id}",
    response_model=schemas.Order,
    tags=["orders"],
    dependencies=[Depends(Etag(deps.order_etag))],
    responses={
        '404': dict(model=schemas.ErrorMessage, description='Order not found'),
        '304': dict(description='Not Modified: Cache hit, ETag not expired')
    }
)
def get_order(order_id: int, db: Session = Depends(deps.get_db)):
    db_order = crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


@router.put(
    "/orders/{order_id}",
    response_model=schemas.Order,
    tags=["orders"],
    dependencies=[Depends(Etag(deps.order_etag))],
    responses={
        '404': dict(model=schemas.ErrorMessage, description='Order not found'),
        '412': dict(description='Unprocessable Entity: ETag has expired')
    }
)
def update_order(
    order_id: int,
    order: schemas.OrderUpdate,
    db: Session = Depends(deps.get_db)
):
    db_order = crud.update_order(db=db, order_id=order_id, order=order)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


@router.delete(
    "/orders/{order_id}",
    status_code=204,
    tags=["orders"],
    dependencies=[Depends(Etag(deps.order_etag))],
    responses={
        '404': dict(model=schemas.ErrorMessage, description='Order not found'),
        '405': dict(
            model=schemas.ErrorMessage,
            description='Method Not Allowed: Order has already been served '
            'or cancelled'
        ),
        '412': dict(description='Unprocessable Entity: ETag has expired')
    }
)
def archive_order(
    order_id: int,
    db: Session = Depends(deps.get_db)
):
    status = crud.archive_order(db, order_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Order not found")

    if status is False:
        raise HTTPException(
            status_code=405,
            detail="Order already served or cancelled"
        )

    return Response(status_code=204)
