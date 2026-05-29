from sqlalchemy.orm import Session
from typing import Optional
from app.models.producto import Producto


class ProductoRepository:
    def get_by_id(self, db: Session, product_id: int) -> Optional[Producto]:
        return db.query(Producto).filter(Producto.id == product_id).first()

    def get_all(self, db: Session, name: Optional[str] = None) -> list[Producto]:
        query = db.query(Producto)
        if name:
            query = query.filter(Producto.nombre.ilike(f"%{name}%"))
        return query.all()

    def create(self, db: Session, data: dict) -> Producto:
        producto = Producto(**data)
        db.add(producto)
        db.commit()
        db.refresh(producto)
        return producto

    def update(self, db: Session, producto: Producto, data: dict) -> Producto:
        for key, value in data.items():
            setattr(producto, key, value)
        db.commit()
        db.refresh(producto)
        return producto

    def delete(self, db: Session, producto: Producto) -> None:
        db.delete(producto)
        db.commit()


producto_repository = ProductoRepository()
