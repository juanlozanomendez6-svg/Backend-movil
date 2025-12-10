# app/routes/auth_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import timedelta
from sqlalchemy.orm import Session
from app.services.auth_service import auth_service
from app.schemas.usuario import UsuarioResponse  # schema de salida
from app.config.session import get_db
# tu dependency para SessionLocal

router = APIRouter(prefix="/auth", tags=["auth"])

# Schema para la respuesta del login
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UsuarioResponse

# Login
@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    result = auth_service.login(db=db, email=form_data.username, password=form_data.password)
    
    if not result or not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_data = result["data"]["user"]
    token = result["data"]["token"]

    return TokenResponse(access_token=token, user=user_data)

# Registro
class RegisterSchema(BaseModel):
    nombre: str
    email: str
    password: str
    rol_id: int = 2  # opcional, default = cliente/admin depende

@router.post("/register", response_model=TokenResponse)
def register(data: RegisterSchema, db: Session = Depends(get_db)):
    result = auth_service.register(
        db=db,
        nombre=data.nombre,
        email=data.email,
        password=data.password,
        rol_id=data.rol_id
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al registrar usuario")
    
    user_data = result["data"]["user"]
    token = result["data"]["token"]

    return TokenResponse(access_token=token, user=user_data)
