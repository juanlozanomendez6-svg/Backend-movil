# app/services/productos_service.py
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from app.models.producto import Producto
from app.models.categoria import Categoria
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

class ProductoService:

    def get_all_products(self, db: Session, categoria_id: int = None, search: str = None):
        try:
            query = db.query(Producto).filter(Producto.activo == True)

            if categoria_id:
                query = query.filter(Producto.categoria_id == categoria_id)

            if search:
                query = query.filter(Producto.nombre.ilike(f"%{search}%"))

            productos = query.order_by(Producto.nombre.asc()).all()

            # opcional: cargar relación categoria
            for p in productos:
                p.categoria

            return {"success": True, "data": productos}

        except SQLAlchemyError as e:
            logger.error(f"Error en ProductoService.get_all_products: {e}")
            raise HTTPException(status_code=500, detail="Error al obtener productos")

    def get_product_by_id(self, db: Session, producto_id: int):
        try:
            producto = db.query(Producto).filter(Producto.id == producto_id).first()
            if not producto:
                raise HTTPException(status_code=404, detail="Producto no encontrado")
            producto.categoria
            return {"success": True, "data": producto}
        except SQLAlchemyError as e:
            logger.error(f"Error en ProductoService.get_product_by_id: {e}")
            raise HTTPException(status_code=500, detail="Error al obtener producto")

    def create_product(self, db: Session, producto_data: dict):
        try:
            producto = Producto(**producto_data)
            db.add(producto)
            db.commit()
            db.refresh(producto)
            producto.categoria
            return {"success": True, "data": producto, "message": "Producto creado exitosamente"}
        except SQLAlchemyError as e:
            logger.error(f"Error en ProductoService.create_product: {e}")
            raise HTTPException(status_code=500, detail="Error al crear producto")

    def update_product(self, db: Session, producto_id: int, producto_data: dict):
        try:
            producto = db.query(Producto).filter(Producto.id == producto_id).first()
            if not producto:
                raise HTTPException(status_code=404, detail="Producto no encontrado")
            for key, value in producto_data.items():
                setattr(producto, key, value)
            db.commit()
            db.refresh(producto)
            producto.categoria
            return {"success": True, "data": producto, "message": "Producto actualizado exitosamente"}
        except SQLAlchemyError as e:
            logger.error(f"Error en ProductoService.update_product: {e}")
            raise HTTPException(status_code=500, detail="Error al actualizar producto")

    def update_stock(self, db: Session, producto_id: int, cantidad: int):
        try:
            producto = db.query(Producto).filter(Producto.id == producto_id).first()
            if not producto:
                raise HTTPException(status_code=404, detail="Producto no encontrado")
            
            nuevo_stock = producto.stock + cantidad
            if nuevo_stock < 0:
                raise HTTPException(status_code=400, detail="Stock insuficiente")
            
            producto.stock = nuevo_stock
            db.commit()
            db.refresh(producto)
            return {"success": True, "data": {"stock": producto.stock}, "message": "Stock actualizado exitosamente"}
        except SQLAlchemyError as e:
            logger.error(f"Error en ProductoService.update_stock: {e}")
            raise HTTPException(status_code=500, detail="Error al actualizar stock")

    def delete_product(self, db: Session, producto_id: int):
        try:
            producto = db.query(Producto).filter(Producto.id == producto_id).first()
            if not producto:
                raise HTTPException(status_code=404, detail="Producto no encontrado")
            
            producto.activo = False
            db.commit()
            return {"success": True, "message": "Producto desactivado exitosamente"}
        except SQLAlchemyError as e:
            logger.error(f"Error en ProductoService.delete_product: {e}")
            raise HTTPException(status_code=500, detail="Error al desactivar producto")


# Instancia única para usar en routers
producto_service = ProductoService()
