from sqlalchemy.orm import Session
from typing import Optional
from app.models.cart import CartItem


class CartRepository:
    def get_by_user(self, db: Session, user_id: int) -> list[CartItem]:
        return (
            db.query(CartItem)
            .filter(CartItem.user_id == user_id)
            .all()
        )

    def get_item(self, db: Session, user_id: int, product_id: int) -> Optional[CartItem]:
        return (
            db.query(CartItem)
            .filter(CartItem.user_id == user_id, CartItem.product_id == product_id)
            .first()
        )

    def add_item(self, db: Session, user_id: int, product_id: int) -> list[CartItem]:
        item = self.get_item(db, user_id, product_id)
        if item:
            item.quantity += 1
        else:
            item = CartItem(user_id=user_id, product_id=product_id, quantity=1)
            db.add(item)
        db.commit()
        return self.get_by_user(db, user_id)

    def remove_item(self, db: Session, user_id: int, product_id: int) -> list[CartItem]:
        item = self.get_item(db, user_id, product_id)
        if item:
            db.delete(item)
            db.commit()
        return self.get_by_user(db, user_id)


cart_repository = CartRepository()
