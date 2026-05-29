from sqlalchemy import Column, Integer, String, Float, Boolean
from app.database import Base


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    precio = Column(Float, nullable=False)
    imagen = Column(String(500), default="")
    categoria = Column(String(50), default="Otros")
    activo = Column(Boolean, default=True)
