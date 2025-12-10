from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
import logging
from app.models.producto_imagen import ProductoImagen

logger = logging.getLogger(__name__)

class ProductoImagenService:

    def get_imagenes_by_producto(self, db: Session, producto_id: int):
        try:
            imagenes = db.query(ProductoImagen).filter(ProductoImagen.producto_id == producto_id).all()
            return {"success": True, "data": imagenes}
        except SQLAlchemyError as e:
            logger.error(f"Error en ProductoImagenService.get_imagenes_by_producto: {e}")
            raise HTTPException(status_code=500, detail="Error al obtener imágenes del producto")

    def get_imagen(self, db: Session, imagen_id: int):
        try:
            imagen = db.query(ProductoImagen).filter(ProductoImagen.id == imagen_id).first()
            if not imagen:
                return {"success": False, "data": None}
            return {"success": True, "data": imagen}
        except SQLAlchemyError as e:
            logger.error(f"Error en ProductoImagenService.get_imagen: {e}")
            raise HTTPException(status_code=500, detail="Error al obtener la imagen")

    def create_imagen(self, db: Session, producto_id: int, imagen_data: dict):
        try:
            imagen_data["producto_id"] = producto_id
            nueva_imagen = ProductoImagen(**imagen_data)
            db.add(nueva_imagen)
            db.commit()
            db.refresh(nueva_imagen)
            return {"success": True, "data": nueva_imagen, "message": "Imagen creada exitosamente"}
        except SQLAlchemyError as e:
            logger.error(f"Error en ProductoImagenService.create_imagen: {e}")
            raise HTTPException(status_code=500, detail="Error al crear la imagen")

    def update_imagen(self, db: Session, imagen_id: int, imagen_data: dict):
        try:
            imagen = db.query(ProductoImagen).filter(ProductoImagen.id == imagen_id).first()
            if not imagen:
                return {"success": False, "data": None}
            for key, value in imagen_data.items():
                setattr(imagen, key, value)
            db.commit()
            db.refresh(imagen)
            return {"success": True, "data": imagen, "message": "Imagen actualizada exitosamente"}
        except SQLAlchemyError as e:
            logger.error(f"Error en ProductoImagenService.update_imagen: {e}")
            raise HTTPException(status_code=500, detail="Error al actualizar la imagen")

    def delete_imagen(self, db: Session, imagen_id: int):
        try:
            imagen = db.query(ProductoImagen).filter(ProductoImagen.id == imagen_id).first()
            if not imagen:
                return {"success": False, "data": None}
            db.delete(imagen)
            db.commit()
            return {"success": True, "message": "Imagen eliminada exitosamente"}
        except SQLAlchemyError as e:
            logger.error(f"Error en ProductoImagenService.delete_imagen: {e}")
            raise HTTPException(status_code=500, detail="Error al eliminar la imagen")


producto_imagen_service = ProductoImagenService()
