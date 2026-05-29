from sqlalchemy.orm import Session
from app.repositories.cart_repository import cart_repository
from app.repositories.producto_repository import producto_repository
from app.services.producto_service import producto_to_dict
from app.exceptions import NotFoundError


def cart_item_to_dict(item) -> dict:
    return {
        "_id": str(item.id),
        "productId": producto_to_dict(item.product),
        "quantity": item.quantity,
    }


def get_cart(db: Session, user_id: int) -> list[dict]:
    items = cart_repository.get_by_user(db, user_id)
    return [cart_item_to_dict(item) for item in items]


def add_to_cart(db: Session, user_id: int, product_id_str: str) -> list[dict]:
    try:
        product_id = int(product_id_str)
    except (ValueError, TypeError):
        raise NotFoundError("ID de producto inválido")

    if not producto_repository.get_by_id(db, product_id):
        raise NotFoundError("Producto no encontrado")

    items = cart_repository.add_item(db, user_id, product_id)
    return [cart_item_to_dict(item) for item in items]


def remove_from_cart(db: Session, user_id: int, product_id_str: str) -> list[dict]:
    try:
        product_id = int(product_id_str)
    except (ValueError, TypeError):
        raise NotFoundError("ID de producto inválido")

    items = cart_repository.remove_item(db, user_id, product_id)
    return [cart_item_to_dict(item) for item in items]
