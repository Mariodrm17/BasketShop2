from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem


class OrderRepository:
    def create(self, db: Session, user_id: int, total: float, items: list[dict]) -> Order:
        order = Order(user_id=user_id, total=total)
        db.add(order)
        db.flush()
        for item in items:
            db.add(OrderItem(order_id=order.id, **item))
        db.commit()
        db.refresh(order)
        return order

    def get_by_user(self, db: Session, user_id: int) -> list[Order]:
        return (
            db.query(Order)
            .filter(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
            .all()
        )

    def get_all(self, db: Session) -> list[Order]:
        return db.query(Order).order_by(Order.created_at.desc()).all()


order_repository = OrderRepository()
