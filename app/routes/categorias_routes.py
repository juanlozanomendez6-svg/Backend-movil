# app/routes/categorias_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.schemas.categoria import CategoriaCreate, CategoriaOut
from app.schemas.common import SuccessResponse
from app.services.categorias_service import categoria_service
from app.config.session import get_db
from app.middleware.auth_middleware import require_roles

# ❌ Antes: prefix="/categorias"
# ✔️ Arreglado:
router = APIRouter(tags=["categorias"])

# -------------------------------
# Rutas públicas
# -------------------------------

@router.get("/", response_model=List[CategoriaOut])
def list_categories(db: Session = Depends(get_db)):
    result = categoria_service.get_all_categorias(db)
    return result["data"]

@router.get("/{categoria_id}", response_model=CategoriaOut)
def get_category(categoria_id: int, db: Session = Depends(get_db)):
    result = categoria_service.get_categoria_by_id(db, categoria_id)
    return result["data"]

# -------------------------------
# Rutas protegidas (solo admin)
# -------------------------------

@router.post("/", response_model=CategoriaOut)
def create_new_category(
    data: CategoriaCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["admin"]))
):
    result = categoria_service.create_categoria(db, data.dict())
    return result["data"]

@router.put("/{categoria_id}", response_model=CategoriaOut)
def update_existing_category(
    categoria_id: int,
    data: CategoriaCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["admin"]))
):
    result = categoria_service.update_categoria(db, categoria_id, data.dict(exclude_unset=True))
    return result["data"]

@router.delete("/{categoria_id}", response_model=SuccessResponse)
def delete_existing_category(
    categoria_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["admin"]))
):
    result = categoria_service.delete_categoria(db, categoria_id)
    return SuccessResponse(**result)
