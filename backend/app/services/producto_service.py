import os
import shutil
import time
from typing import Optional

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.repositories.producto_repository import producto_repository
from app.exceptions import NotFoundError
from app.config import settings


def producto_to_dict(p) -> dict:
    return {
        "_id": str(p.id),
        "nombre": p.nombre,
        "precio": p.precio,
        "imagen": p.imagen or "",
        "categoria": p.categoria,
        "activo": p.activo,
    }


def get_productos(db: Session, name: Optional[str] = None) -> list[dict]:
    return [producto_to_dict(p) for p in producto_repository.get_all(db, name)]


async def create_producto(
    db: Session,
    nombre: str,
    precio: float,
    categoria: str = "Otros",
    imagen_file: Optional[UploadFile] = None,
    imagen_url: Optional[str] = None,
) -> dict:
    imagen = ""
    if imagen_file and imagen_file.filename:
        ext = os.path.splitext(imagen_file.filename)[1]
        filename = f"{int(time.time() * 1000)}{ext}"
        dest = os.path.join(settings.UPLOAD_DIR, filename)
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        with open(dest, "wb") as f:
            shutil.copyfileobj(imagen_file.file, f)
        imagen = filename
    elif imagen_url:
        imagen = imagen_url

    product = producto_repository.create(
        db,
        {"nombre": nombre, "precio": precio, "imagen": imagen, "categoria": categoria, "activo": True},
    )
    return producto_to_dict(product)


def update_producto(db: Session, product_id: str, data: dict) -> dict:
    try:
        pid = int(product_id)
    except ValueError:
        raise NotFoundError("ID de producto inválido")

    product = producto_repository.get_by_id(db, pid)
    if not product:
        raise NotFoundError("Producto no encontrado")

    if data:
        product = producto_repository.update(db, product, data)

    return producto_to_dict(product)


def delete_producto(db: Session, product_id: str) -> None:
    try:
        pid = int(product_id)
    except ValueError:
        raise NotFoundError("ID de producto inválido")

    product = producto_repository.get_by_id(db, pid)
    if not product:
        raise NotFoundError("Producto no encontrado")
    producto_repository.delete(db, product)
