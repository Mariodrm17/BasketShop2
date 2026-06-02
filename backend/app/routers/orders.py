from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.order_service import checkout, get_user_orders, get_all_orders
from app.dependencies.auth import get_current_user, get_current_admin
from app.exceptions import NotFoundError

router = APIRouter()


@router.post("/orders/checkout", status_code=201)
def checkout_endpoint(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return checkout(db, current_user.id)
    except NotFoundError as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.get("/orders/my")
def my_orders(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return get_user_orders(db, current_user.id)


@router.get("/orders")
def all_orders(current_user=Depends(get_current_admin), db: Session = Depends(get_db)):
    return get_all_orders(db)
