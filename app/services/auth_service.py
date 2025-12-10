# app/services/auth_service.py
from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.utils.helpers import hash_password, verify_password
from app.utils.jwt import create_access_token
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)

class AuthService:
    def register(self, db: Session, nombre: str, email: str, password: str, rol_id: int = 2):
        try:
            existing_user = db.query(Usuario).filter(Usuario.email == email).first()
            if existing_user:
                raise HTTPException(status_code=400, detail="El usuario ya existe")

            password_hash = hash_password(password)
            usuario = Usuario(
                nombre=nombre,
                email=email,
                password_hash=password_hash,
                rol_id=rol_id
            )
            db.add(usuario)
            db.commit()
            db.refresh(usuario)

            token = create_access_token({
                "sub": str(usuario.id),
                "email": usuario.email,
                "rol": usuario.rol_id
            })

            return {
                "success": True,
                "data": {
                    "user": {
                        "id": usuario.id,
                        "nombre": usuario.nombre,
                        "email": usuario.email,
                        "rol_id": usuario.rol_id
                    },
                    "token": token
                },
                "message": "Usuario registrado exitosamente"
            }
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Error en AuthService.register: {e}")
            raise HTTPException(status_code=500, detail="Error al registrar usuario")

    def login(self, db: Session, email: str, password: str):
        try:
            usuario = db.query(Usuario).filter(Usuario.email == email).first()
            if not usuario:
                raise HTTPException(status_code=401, detail="Credenciales inválidas")
            if not usuario.activo:
                raise HTTPException(status_code=403, detail="Usuario inactivo")
            if not verify_password(password, usuario.password_hash):
                raise HTTPException(status_code=401, detail="Credenciales inválidas")

            rol = db.query(Rol).filter(Rol.id == usuario.rol_id).first()

            token = create_access_token({
                "sub": str(usuario.id),
                "email": usuario.email,
                "rol": usuario.rol_id,
                "rol_nombre": rol.nombre if rol else None
            })

            return {
                "success": True,
                "data": {
                    "user": {
                        "id": usuario.id,
                        "nombre": usuario.nombre,
                        "email": usuario.email,
                        "rol_id": usuario.rol_id,
                        "rol_nombre": rol.nombre if rol else None
                    },
                    "token": token
                },
                "message": "Login exitoso"
            }
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Error en AuthService.login: {e}")
            raise HTTPException(status_code=500, detail="Error en el login")

    def get_profile(self, db: Session, user_id: int):
        try:
            usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
            if not usuario:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            
            rol = db.query(Rol).filter(Rol.id == usuario.rol_id).first()
            
            return {
                "success": True,
                "data": {
                    "id": usuario.id,
                    "nombre": usuario.nombre,
                    "email": usuario.email,
                    "rol_id": usuario.rol_id,
                    "rol_nombre": rol.nombre if rol else None
                }
            }
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Error en AuthService.get_profile: {e}")
            raise HTTPException(status_code=500, detail="Error al obtener perfil")


# Instancia única, como en tu versión de Node
auth_service = AuthService()
