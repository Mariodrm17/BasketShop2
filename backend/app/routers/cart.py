from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.producto import CartItemRequest
from app.services.cart_service import get_cart, add_to_cart, remove_from_cart
from app.dependencies.auth import get_current_user
from app.exceptions import NotFoundError

router = APIRouter()


@router.get("/cart")
def get_cart_endpoint(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_cart(db, current_user.id)


@router.post("/cart/add")
def add_to_cart_endpoint(
    body: CartItemRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return add_to_cart(db, current_user.id, body.productId)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.delete("/cart/{product_id}")
def remove_from_cart_endpoint(
    product_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return remove_from_cart(db, current_user.id, product_id)
