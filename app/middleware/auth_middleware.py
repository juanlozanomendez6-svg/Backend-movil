# app/middleware/auth_middleware.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import List
from app.utils.jwt import verify_token  # Debes implementar verify_token en Python
from app.models.usuario import Usuario  # opcional para obtener info de BD

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Verifica el token y devuelve los datos del usuario autenticado.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de acceso requerido"
        )
    try:
        user_data = verify_token(token)  # {id, email, rol}
        return user_data
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token inválido o expirado"
        )

def require_roles(allowed_roles: List[str], allow_self: bool = False):
    """
    Verifica que el usuario tenga un rol permitido o que esté actuando sobre sí mismo.
    Uso: Depends(require_roles(["admin", "supervisor"]))
    """
    def role_checker(current_user: dict = Depends(get_current_user), id: int = None):
        is_allowed_role = current_user.get("rol") in allowed_roles
        is_self = allow_self and id is not None and current_user.get("id") == id

        if not is_allowed_role and not is_self:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para realizar esta acción"
            )
        return current_user

    return role_checker
