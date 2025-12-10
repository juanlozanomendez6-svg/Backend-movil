# app/routes/productos_routes.py

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from app.schemas.producto import ProductoCreate, ProductoResponse, StockUpdate, ProductoUpdate
from app.services.productos_service import producto_service
from app.middleware.auth_middleware import require_roles
from app.config.session import get_db

productos_router = APIRouter(tags=["productos"])


# ================================
#           LISTAR
# ================================
@productos_router.get("/", response_model=List[ProductoResponse])
def list_products(db: Session = Depends(get_db)):
    result = producto_service.get_all_products(db)
    productos = result.get("data", [])
    if not productos:
        raise HTTPException(status_code=404, detail="No se encontraron productos")
    return productos


@productos_router.get("/{producto_id}", response_model=ProductoResponse)
def get_product(producto_id: int, db: Session = Depends(get_db)):
    result = producto_service.get_product_by_id(db, producto_id)
    producto = result.get("data")
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


# ================================
#           CREAR
# ================================
@productos_router.post("/", response_model=ProductoResponse)
def create_new_product(
    data: ProductoCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["admin", "supervisor"]))
):
    # CORRECCIÓN IMPORTANTE:
    result = producto_service.create_product(db, data.model_dump())

    producto = result.get("data")
    if not producto:
        raise HTTPException(status_code=400, detail="No se pudo crear el producto")
    return producto


# ================================
#           ACTUALIZAR
# ================================
@productos_router.put("/{producto_id}", response_model=ProductoResponse)
def update_existing_product(
    producto_id: int,
    data: ProductoUpdate,  # <-- AHORA el correcto
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["admin", "supervisor"]))
):

    result = producto_service.update_product(
        db,
        producto_id,
        data.model_dump(exclude_unset=True)  # CORRECCIÓN
    )

    producto = result.get("data")
    if not producto:
        raise HTTPException(status_code=400, detail="No se pudo actualizar el producto")
    return producto


# ================================
#           ACTUALIZAR STOCK
# ================================
@productos_router.patch("/{producto_id}/stock", response_model=ProductoResponse)
def modify_stock(
    producto_id: int,
    data: StockUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["admin", "supervisor"]))
):

    result = producto_service.update_stock(db, producto_id, data.stock)
    producto = result.get("data")
    if not producto:
        raise HTTPException(status_code=400, detail="No se pudo actualizar el stock")
    return producto


# ================================
#           ELIMINAR
# ================================
@productos_router.delete("/{producto_id}", response_model=dict)
def delete_existing_product(
    producto_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["admin"]))
):

    result = producto_service.delete_product(db, producto_id)

    if not result:
        raise HTTPException(status_code=400, detail="No se pudo eliminar el producto")

    return {
        "success": True,
        "message": "Producto eliminado correctamente"
    }
