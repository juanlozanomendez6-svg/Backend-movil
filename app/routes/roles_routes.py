# app/routes/roles_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.schemas.rol import RolCreate, RolUpdate, RolResponse
from app.services.roles_service import rol_service
from app.middleware.auth_middleware import require_roles
from app.config.db import get_db  # <-- inyectamos la sesión

router = APIRouter(tags=["roles"])

# Obtener todos los roles
@router.get("/", response_model=List[RolResponse])
def list_roles(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["admin"]))
):
    result = rol_service.get_all_roles(db)
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron roles"
        )
    return result["data"]

# Obtener rol por ID
@router.get("/{rol_id}", response_model=RolResponse)
def get_role(
    rol_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["admin"]))
):
    result = rol_service.get_rol_by_id(db, rol_id)
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )
    return result["data"]

# Crear rol
@router.post("/", response_model=RolResponse, status_code=status.HTTP_201_CREATED)
def create_new_role(
    data: RolCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["admin"]))
):
    result = rol_service.create_rol(db, data.dict())
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo crear el rol"
        )
    return result["data"]

# Actualizar rol
@router.put("/{rol_id}", response_model=RolResponse)
def update_existing_role(
    rol_id: int,
    data: RolUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["admin"]))
):
    result = rol_service.update_rol(db, rol_id, data.dict())
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo actualizar el rol"
        )
    return result["data"]

# Eliminar rol
@router.delete("/{rol_id}", response_model=dict)
def delete_existing_role(
    rol_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["admin"]))
):
    result = rol_service.delete_rol(db, rol_id)
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo eliminar el rol"
        )
    return {"success": True, "message": "Rol eliminado correctamente"}
