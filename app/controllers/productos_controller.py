# app/routes/productos_routes.py
from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional
from app.services.productos_service import (
    get_all_products,
    get_product_by_id,
    create_product,
    update_product,
    update_stock,
    delete_product
)
from app.schemas.producto import ProductoCreate, ProductoResponse, StockUpdate
from app.middleware.auth_middleware import require_roles

router = APIRouter(prefix="/productos", tags=["productos"])

@router.get("/", response_model=List[ProductoResponse])
def list_products(
    categoria_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None)
):
    filters = {"categoria_id": categoria_id, "search": search}
    return get_all_products(filters)

@router.get("/{producto_id}", response_model=ProductoResponse)
def get_product(producto_id: int):
    product = get_product_by_id(producto_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@router.post("/", response_model=ProductoResponse)
def create_new_product(
    data: ProductoCreate,
    current_user=Depends(require_roles([1, 2]))  # admin o supervisor
):
    return create_product(data.dict())

@router.put("/{producto_id}", response_model=ProductoResponse)
def update_existing_product(
    producto_id: int,
    data: ProductoCreate,
    current_user=Depends(require_roles([1, 2]))
):
    return update_product(producto_id, data.dict())

@router.patch("/{producto_id}/stock", response_model=ProductoResponse)
def modify_stock(
    producto_id: int,
    data: StockUpdate,
    current_user=Depends(require_roles([1, 2]))
):
    return update_stock(producto_id, data.stock)

@router.delete("/{producto_id}")
def delete_existing_product(
    producto_id: int,
    current_user=Depends(require_roles([1]))  # solo admin
):
    return delete_product(producto_id)
