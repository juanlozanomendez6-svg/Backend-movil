# app/controllers/producto_imagen_controller.py
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas.producto_imagen import ProductoImagenCreate, ProductoImagenUpdate, ProductoImagenResponse
from app.services.producto_imagen_service import producto_imagen_service
from app.config.session import get_db

class ProductoImagenController:

    @staticmethod
    def listar(producto_id: int, db: Session = Depends(get_db)) -> List[ProductoImagenResponse]:
        result = producto_imagen_service.get_imagenes_by_producto(db, producto_id)
        imagenes = result.get("data", [])
        if not imagenes:
            raise HTTPException(status_code=404, detail="No se encontraron imágenes para este producto")
        return imagenes

    @staticmethod
    def obtener(producto_id: int, imagen_id: int, db: Session = Depends(get_db)) -> ProductoImagenResponse:
        result = producto_imagen_service.get_imagen(db, imagen_id)
        imagen = result.get("data")
        if not imagen:
            raise HTTPException(status_code=404, detail="Imagen no encontrada")
        return imagen

    @staticmethod
    def crear(producto_id: int, data: ProductoImagenCreate, db: Session = Depends(get_db)) -> ProductoImagenResponse:
        result = producto_imagen_service.create_imagen(db, producto_id, data.model_dump())
        imagen = result.get("data")
        if not imagen:
            raise HTTPException(status_code=400, detail="No se pudo crear la imagen")
        return imagen

    @staticmethod
    def actualizar(producto_id: int, imagen_id: int, data: ProductoImagenUpdate, db: Session = Depends(get_db)) -> ProductoImagenResponse:
        result = producto_imagen_service.update_imagen(db, imagen_id, data.model_dump(exclude_unset=True))
        imagen = result.get("data")
        if not imagen:
            raise HTTPException(status_code=400, detail="No se pudo actualizar la imagen")
        return imagen

    @staticmethod
    def eliminar(producto_id: int, imagen_id: int, db: Session = Depends(get_db)) -> dict:
        result = producto_imagen_service.delete_imagen(db, imagen_id)
        if not result.get("success", False):
            raise HTTPException(status_code=400, detail="No se pudo eliminar la imagen")
        return {"success": True, "message": "Imagen eliminada correctamente"}
