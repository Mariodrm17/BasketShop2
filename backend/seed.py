"""
Script de inicialización de datos.
Ejecutar una sola vez: python seed.py (desde la carpeta backend/)
"""
from app import models  # noqa: F401
from app.database import SessionLocal, engine, Base
from app.repositories.user_repository import user_repository
from app.repositories.producto_repository import producto_repository
from app.services.auth_service import hash_password


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Usuarios por defecto
    if not user_repository.get_by_username(db, "admin"):
        user_repository.create(db, "admin", hash_password("admin123"), "admin")
        print("  admin / admin123  (rol: admin)")

    if not user_repository.get_by_username(db, "user"):
        user_repository.create(db, "user", hash_password("user123"), "user")
        print("  user  / user123   (rol: user)")

    # Productos de ejemplo
    if not producto_repository.get_all(db):
        samples = [
            {"nombre": "Nike Air Max 90", "precio": 119.99, "imagen": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400", "categoria": "Zapatillas", "activo": True},
            {"nombre": "Adidas Ultraboost 22", "precio": 149.99, "imagen": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400", "categoria": "Zapatillas", "activo": True},
            {"nombre": "Camiseta NBA Lakers", "precio": 39.99, "imagen": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=400", "categoria": "Ropa", "activo": True},
            {"nombre": "Balón NBA Official", "precio": 89.99, "imagen": "https://images.unsplash.com/photo-1546519638405-a9f3e4c5f9a1?w=400", "categoria": "Balones", "activo": True},
            {"nombre": "Gorra NBA Bulls", "precio": 24.99, "imagen": "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=400", "categoria": "Accesorios", "activo": True},
        ]
        for p in samples:
            producto_repository.create(db, p)
        print(f"  {len(samples)} productos de ejemplo creados")

    db.close()
    print("\nSeed completado.")


if __name__ == "__main__":
    print("Creando datos iniciales...\n")
    seed()
