from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import LoginRequest, RegisterRequest, TokenResponse
from app.services.auth_service import login, register
from app.exceptions import UnauthorizedError, ConflictError

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login_endpoint(data: LoginRequest, db: Session = Depends(get_db)):
    try:
        token = login(db, data.username, data.password)
        return {"token": token}
    except UnauthorizedError as e:
        raise HTTPException(status_code=401, detail=e.message)


@router.post("/register", status_code=201)
def register_endpoint(data: RegisterRequest, db: Session = Depends(get_db)):
    try:
        register(db, data.username, data.password)
        return {"message": "Usuario registrado con éxito"}
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=e.message)
