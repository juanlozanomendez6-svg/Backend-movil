# app/routes/categorias_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.services.categorias_service import (
    get_all_categories,
    get_category_by_id,
    create_category,
    update_category,
    delete_category
)
from app.schemas.categoria import CategoriaCreate, CategoriaResponse
from app.middleware.auth_middleware import require_roles

router = APIRouter(prefix="/categorias", tags=["categorias"])

@router.get("/", response_model=List[CategoriaResponse])
def list_categories():
    return get_all_categories()

@router.get("/{categoria_id}", response_model=CategoriaResponse)
def get_category(categoria_id: int):
    category = get_category_by_id(categoria_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    return category

@router.post("/", response_model=CategoriaResponse)
def create_new_category(data: CategoriaCreate, current_user=Depends(require_roles([1]))):  # 1 = admin
    return create_category(data.dict())

@router.put("/{categoria_id}", response_model=CategoriaResponse)
def update_existing_category(categoria_id: int, data: CategoriaCreate, current_user=Depends(require_roles([1]))):
    updated = update_category(categoria_id, data.dict())
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    return updated

@router.delete("/{categoria_id}")
def delete_existing_category(categoria_id: int, current_user=Depends(require_roles([1]))):
    deleted = delete_category(categoria_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    return {"success": True, "message": "Categoría eliminada correctamente"}
