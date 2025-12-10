from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from pydantic import BaseModel
from bson import ObjectId

from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioOut
from app.services.usuarios_service import usuario_service_mongo as usuario_service
from app.middleware.auth_middleware import require_roles

# Router
router = APIRouter(tags=["usuarios"])  # prefix se maneja en app.py

# Schemas adicionales
class LoginSchema(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UsuarioOut

# -------------------------------
# Rutas públicas
# -------------------------------
@router.post("/login", response_model=TokenResponse)
def login_user_route(data: LoginSchema):
    result = usuario_service.login(data.email, data.password)
    if not result.get("success"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    user = result["data"]["usuario"]
    token = result["data"]["token"]
    # Convertir ObjectId a str
    user["_id"] = str(user["_id"])
    return TokenResponse(access_token=token, user=user)

@router.post("/register", response_model=UsuarioOut)
def register_user_route(data: UsuarioCreate):
    result = usuario_service.register(data.nombre, data.email, data.password, data.rol_id)
    usuario = result["data"]["usuario"]
    usuario["_id"] = str(usuario["_id"])
    return usuario

# -------------------------------
# Rutas protegidas
# -------------------------------
@router.get("/", response_model=List[UsuarioOut])
def list_users_route(current_user=Depends(require_roles(["admin"]))):
    usuarios = usuario_service.list_all()
    # Convertir ObjectId a str en todos los usuarios
    return [
        {
            "_id": str(u["_id"]),
            "nombre": u["nombre"],
            "email": u["email"],
            "rol_id": u["rol_id"],
            "activo": u["activo"]
        }
        for u in usuarios
    ]

@router.get("/{usuario_id}", response_model=UsuarioOut)
def get_user_route(usuario_id: str, current_user=Depends(require_roles(["admin", "supervisor"], allow_self=True))):
    usuario = usuario_service.get_by_id(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario["_id"] = str(usuario["_id"])
    return usuario

@router.put("/{usuario_id}", response_model=UsuarioOut)
def update_user_route(usuario_id: str, data: UsuarioUpdate, current_user=Depends(require_roles(["admin"], allow_self=True))):
    usuario = usuario_service.update(usuario_id, data.dict(exclude_unset=True))
    usuario["_id"] = str(usuario["_id"])
    return usuario

@router.delete("/{usuario_id}", response_model=dict)
def delete_user_route(usuario_id: str, current_user=Depends(require_roles(["admin"]))):
    result = usuario_service.delete(usuario_id)
    return {"success": result.get("success", False), "message": result.get("message", "")}

# Exportar router
usuarios_router = router
