from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.rol import RolCreate, RolUpdate, RolResponse
from app.services.roles_service import rol_service
from app.middleware.auth_middleware import require_roles

router = APIRouter(prefix="/roles", tags=["roles"])

# Obtener todos los roles
@router.get("/", response_model=List[RolResponse])
def list_roles(current_user=Depends(require_roles(["admin"]))):
    result = rol_service.get_all_roles()
    return result["data"] if result["success"] else []

# Obtener rol por ID
@router.get("/{rol_id}", response_model=RolResponse)
def get_role(rol_id: int, current_user=Depends(require_roles(["admin"]))):
    result = rol_service.get_rol_by_id(rol_id)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado")
    return result["data"]

# Crear rol
@router.post("/", response_model=RolResponse, status_code=status.HTTP_201_CREATED)
def create_new_role(data: RolCreate, current_user=Depends(require_roles(["admin"]))):
    result = rol_service.create_rol(data.dict())
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se pudo crear el rol")
    return result["data"]

# Actualizar rol
@router.put("/{rol_id}", response_model=RolResponse)
def update_existing_role(rol_id: int, data: RolUpdate, current_user=Depends(require_roles(["admin"]))):
    result = rol_service.update_rol(rol_id, data.dict())
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se pudo actualizar el rol")
    return result["data"]

# Eliminar rol
@router.delete("/{rol_id}", response_model=dict)
def delete_existing_role(rol_id: int, current_user=Depends(require_roles(["admin"]))):
    result = rol_service.delete_rol(rol_id)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se pudo eliminar el rol")
    return {"success": True, "message": "Rol eliminado correctamente"}
