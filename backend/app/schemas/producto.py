from pydantic import BaseModel, field_validator
from typing import Optional

CATEGORIAS_VALIDAS = ["Zapatillas", "Ropa", "Accesorios", "Balones", "Otros"]


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None
    imagen: Optional[str] = None
    categoria: Optional[str] = None
    activo: Optional[bool] = None

    @field_validator("nombre")
    @classmethod
    def nombre_not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.strip() if v else v

    @field_validator("precio")
    @classmethod
    def precio_positive(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v < 0:
            raise ValueError("El precio no puede ser negativo")
        return v

    @field_validator("categoria")
    @classmethod
    def categoria_valid(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in CATEGORIAS_VALIDAS:
            raise ValueError(f"Categoría debe ser una de: {', '.join(CATEGORIAS_VALIDAS)}")
        return v


class CartItemRequest(BaseModel):
    productId: str
