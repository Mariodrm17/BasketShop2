from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.schemas.producto import ProductoUpdate
from app.services.producto_service import get_productos, get_producto, create_producto, update_producto, delete_producto
from app.dependencies.auth import get_current_admin
from app.exceptions import NotFoundError

router = APIRouter()


@router.get("/productos")
def list_productos(name: Optional[str] = None, db: Session = Depends(get_db)):
    return get_productos(db, name)


@router.get("/productos/{product_id}")
def get_producto_endpoint(product_id: str, db: Session = Depends(get_db)):
    try:
        return get_producto(db, product_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.post("/productos", status_code=201)
async def create_producto_endpoint(
    nombre: str = Form(...),
    precio: float = Form(...),
    categoria: str = Form("Otros"),
    imagen: Optional[UploadFile] = File(None),
    imagenUrl: Optional[str] = Form(None),
    current_user=Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    if precio < 0:
        raise HTTPException(status_code=422, detail="El precio no puede ser negativo")
    if not nombre.strip():
        raise HTTPException(status_code=422, detail="El nombre no puede estar vacío")
    return await create_producto(db, nombre.strip(), precio, categoria, imagen, imagenUrl)


@router.put("/productos/{product_id}")
def update_producto_endpoint(
    product_id: str,
    data: ProductoUpdate,
    current_user=Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    try:
        return update_producto(db, product_id, data.model_dump(exclude_unset=True))
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.delete("/productos/{product_id}")
def delete_producto_endpoint(
    product_id: str,
    current_user=Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    try:
        delete_producto(db, product_id)
        return {"message": "Producto eliminado"}
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
