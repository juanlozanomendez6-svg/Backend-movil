# app/services/inventario_service.py
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from app.models.producto import Producto
from app.models.inventario_historial import InventarioHistorial
from app.models.usuario import Usuario
from fastapi import HTTPException
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class InventarioService:

    def get_inventory_history(self, db: Session, producto_id: int = None, fecha_inicio: datetime = None, fecha_fin: datetime = None):
        try:
            query = db.query(InventarioHistorial)
            
            if producto_id:
                query = query.filter(InventarioHistorial.producto_id == producto_id)
            
            if fecha_inicio and fecha_fin:
                query = query.filter(InventarioHistorial.fecha.between(fecha_inicio, fecha_fin))
            
            historial = query.order_by(InventarioHistorial.fecha.desc()).all()
            
            # Opcional: cargar relaciones
            for movimiento in historial:
                movimiento.producto  # relación Producto
                movimiento.usuario   # relación Usuario

            return {"success": True, "data": historial}

        except Exception as e:
            logger.error(f"Error en InventarioService.get_inventory_history: {e}")
            raise HTTPException(status_code=500, detail="Error al obtener historial")

    def register_movement(self, db: Session, producto_id: int, usuario_id: int, cambio: int, motivo: str):
        try:
            producto = db.query(Producto).filter(Producto.id == producto_id).first()
            if not producto:
                raise HTTPException(status_code=404, detail="Producto no encontrado")
            
            if cambio < 0 and abs(cambio) > producto.stock:
                raise HTTPException(status_code=400, detail="Stock insuficiente")

            movimiento = InventarioHistorial(
                producto_id=producto_id,
                usuario_id=usuario_id,
                cambio=cambio,
                motivo=motivo
            )
            db.add(movimiento)

            if motivo != 'venta':
                producto.stock += cambio

            db.commit()
            db.refresh(movimiento)
            return {"success": True, "data": movimiento, "message": "Movimiento registrado exitosamente"}

        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Error en InventarioService.register_movement: {e}")
            raise HTTPException(status_code=500, detail="Error al registrar movimiento")

    def get_low_stock(self, db: Session, umbral: int = 10):
        try:
            productos = db.query(Producto).filter(
                Producto.stock <= umbral,
                Producto.activo == True
            ).order_by(Producto.stock.asc()).all()

            message = None
            if len(productos) == 0:
                message = "No hay productos con stock bajo"

            return {"success": True, "data": productos, "message": message}

        except Exception as e:
            logger.error(f"Error en InventarioService.get_low_stock: {e}")
            raise HTTPException(status_code=500, detail="Error al obtener productos con stock bajo")

    def get_inventory_statistics(self, db: Session):
        try:
            total_productos = db.query(func.count(Producto.id)).filter(Producto.activo == True).scalar()
            productos_stock_bajo = db.query(func.count(Producto.id)).filter(Producto.stock <= 10, Producto.activo == True).scalar()
            productos_sin_stock = db.query(func.count(Producto.id)).filter(Producto.stock == 0, Producto.activo == True).scalar()
            valor_total_inventario = db.query(func.sum(Producto.precio)).filter(Producto.activo == True).scalar() or 0

            return {
                "success": True,
                "data": {
                    "totalProductos": total_productos,
                    "productosStockBajo": productos_stock_bajo,
                    "productosSinStock": productos_sin_stock,
                    "valorTotalInventario": valor_total_inventario
                }
            }
        except Exception as e:
            logger.error(f"Error en InventarioService.get_inventory_statistics: {e}")
            raise HTTPException(status_code=500, detail="Error al obtener estadísticas")


# Instancia única
inventario_service = InventarioService()
