from sqlalchemy.orm import Session
from app.repositories.order_repository import order_repository
from app.repositories.cart_repository import cart_repository
from app.exceptions import NotFoundError


def order_to_dict(order) -> dict:
    return {
        "_id": str(order.id),
        "userId": str(order.user_id),
        "username": order.user.username if order.user else "?",
        "total": order.total,
        "createdAt": order.created_at.isoformat(),
        "items": [
            {
                "_id": str(i.id),
                "productId": str(i.product_id) if i.product_id else None,
                "productName": i.product_name,
                "productPrice": i.product_price,
                "quantity": i.quantity,
            }
            for i in order.items
        ],
    }


def checkout(db: Session, user_id: int) -> dict:
    cart_items = cart_repository.get_by_user(db, user_id)
    if not cart_items:
        raise NotFoundError("El carrito está vacío")

    items = []
    total = 0.0
    for ci in cart_items:
        if not ci.product:
            continue
        items.append({
            "product_id": ci.product_id,
            "product_name": ci.product.nombre,
            "product_price": ci.product.precio,
            "quantity": ci.quantity,
        })
        total += ci.product.precio * ci.quantity

    order = order_repository.create(db, user_id, round(total, 2), items)
    cart_repository.clear(db, user_id)
    return order_to_dict(order)


def get_user_orders(db: Session, user_id: int) -> list[dict]:
    return [order_to_dict(o) for o in order_repository.get_by_user(db, user_id)]


def get_all_orders(db: Session) -> list[dict]:
    return [order_to_dict(o) for o in order_repository.get_all(db)]
