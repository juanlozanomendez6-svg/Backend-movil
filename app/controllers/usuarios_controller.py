from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioOut, UsuarioLogin
from app.services.usuarios_service import usuario_service

def get_all_users(db: Session):
    result = usuario_service.get_all_usuarios(db)
    return result["data"]

def get_user_by_id(db: Session, user_id: int):
    result = usuario_service.get_usuario_by_id(db, user_id)
    return result["data"]

def register_user(db: Session, data: UsuarioCreate):
    result = usuario_service.register(
        db=db,
        nombre=data.nombre,
        email=data.email,
        password=data.password,
        rol_id=data.rol_id
    )
    return result["data"]["usuario"]

def update_user(db: Session, user_id: int, data: UsuarioUpdate):
    result = usuario_service.update_usuario(db, user_id, data.dict(exclude_unset=True))
    return result["data"]

def delete_user(db: Session, user_id: int):
    result = usuario_service.delete_usuario(db, user_id)
    return result

def login_user(db: Session, data: UsuarioLogin):
    result = usuario_service.login(db, data.email, data.password)
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    return {
        "user": result["data"]["usuario"],
        "token": result["data"]["token"]
    }
