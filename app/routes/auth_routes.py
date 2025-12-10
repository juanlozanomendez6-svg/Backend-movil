# app/routes/auth_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.services.auth_service import auth_service
from app.schemas.usuario import UsuarioOut  # Schema de salida correcto
from app.config.session import get_db  # Dependency para SessionLocal
from app.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

# -------------------------------
# Schemas
# -------------------------------
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UsuarioOut

class RegisterSchema(BaseModel):
    nombre: str
    email: str
    password: str
    rol_id: int = 2  # Default: cliente/admin según tu lógica

# Para perfil del usuario autenticado
class UserProfileSchema(BaseModel):
    id: int
    nombre: str
    email: str
    rol_id: int
    rol_nombre: str | None = None

# -------------------------------
# Rutas públicas
# -------------------------------

@router.post("/register", response_model=TokenResponse)
def register(data: RegisterSchema, db: Session = Depends(get_db)):
    """
    Registro de usuario.
    """
    result = auth_service.register(
        db=db,
        nombre=data.nombre,
        email=data.email,
        password=data.password,
        rol_id=data.rol_id
    )

    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al registrar usuario"
        )

    user_data = result["data"]["user"]
    token = result["data"]["token"]

    return TokenResponse(access_token=token, user=user_data)

@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login de usuario.
    """
    result = auth_service.login(db=db, email=form_data.username, password=form_data.password)

    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_data = result["data"]["user"]
    token = result["data"]["token"]

    return TokenResponse(access_token=token, user=user_data)

# -------------------------------
# Rutas protegidas
# -------------------------------

@router.get("/profile", response_model=UserProfileSchema)
def profile(current_user=Depends(get_current_user)):
    """
    Obtener datos del usuario autenticado.
    """
    db: Session = current_user["db"]
    user_id: int = current_user["id"]
    return auth_service.get_profile(db=db, user_id=user_id)

@router.get("/verify", response_model=UserProfileSchema)
def verify(current_user=Depends(get_current_user)):
    """
    Verifica que el token sea válido y devuelve info del usuario.
    """
    return current_user
