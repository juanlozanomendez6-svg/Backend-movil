from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.schemas.producto_imagen import ProductoImagenCreate, ProductoImagenUpdate, ProductoImagenResponse
from app.services.producto_imagen_service import producto_imagen_service
from app.middleware.auth_middleware import require_roles
from app.config.session import get_db

producto_imagen_router = APIRouter(tags=["imagenes"])

# ================================
# LISTAR
# ================================
@producto_imagen_router.get("/", response_model=List[ProductoImagenResponse])
def listar_imagenes_producto(
    producto_id: int,
    db: Session = Depends(get_db)
):
    result = producto_imagen_service.get_imagenes_by_producto(db, producto_id)
    imagenes = result.get("data", [])
    # No lanzar HTTPException si no hay imágenes, simplemente devolver []
    return imagenes
# ================================
# OBTENER
# ================================
@producto_imagen_router.get("/{imagen_id}", response_model=ProductoImagenResponse)
def obtener_imagen_producto(producto_id: int, imagen_id: int, db: Session = Depends(get_db)):
    result = producto_imagen_service.get_imagen(db, imagen_id)
    imagen = result.get("data")
    if not imagen:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    return imagen

# ================================
# CREAR
# ================================
@producto_imagen_router.post("/", response_model=ProductoImagenResponse, status_code=status.HTTP_201_CREATED)
def crear_imagen_producto(
    producto_id: int,
    data: ProductoImagenCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["admin", "supervisor"]))
):
    result = producto_imagen_service.create_imagen(db, producto_id, data.model_dump())
    imagen = result.get("data")
    if not imagen:
        raise HTTPException(status_code=400, detail="No se pudo crear la imagen")
    return imagen

# ================================
# ACTUALIZAR
# ================================
@producto_imagen_router.put("/{imagen_id}", response_model=ProductoImagenResponse)
def actualizar_imagen_producto(
    producto_id: int,
    imagen_id: int,
    data: ProductoImagenUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["admin", "supervisor"]))
):
    result = producto_imagen_service.update_imagen(db, imagen_id, data.model_dump(exclude_unset=True))
    imagen = result.get("data")
    if not imagen:
        raise HTTPException(status_code=400, detail="No se pudo actualizar la imagen")
    return imagen

# ================================
# ELIMINAR
# ================================
@producto_imagen_router.delete("/{imagen_id}", response_model=dict)
def eliminar_imagen_producto(
    producto_id: int,
    imagen_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["admin"]))
):
    result = producto_imagen_service.delete_imagen(db, imagen_id)
    if not result:
        raise HTTPException(status_code=400, detail="No se pudo eliminar la imagen")
    return {
        "success": True,
        "message": "Imagen eliminada correctamente"
    }
