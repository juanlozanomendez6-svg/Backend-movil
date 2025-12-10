# app/services/ventas_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, between
from app.models.venta import Venta
from app.models.detalle_venta import DetalleVenta
from app.models.producto import Producto
from app.models.usuario import Usuario
from app.schemas.venta import VentaCreate
import logging

logger = logging.getLogger(__name__)

class VentaService:

    def get_all_ventas(self, db: Session, filters: dict = {}):
        try:
            query = db.query(Venta)

            if filters.get("fecha_inicio") and filters.get("fecha_fin"):
                query = query.filter(Venta.fecha.between(filters["fecha_inicio"], filters["fecha_fin"]))

            if filters.get("usuario_id"):
                query = query.filter(Venta.usuario_id == filters["usuario_id"])

            ventas = query.order_by(Venta.fecha.desc()).all()
            for venta in ventas:
                venta.usuario  # cargar relación usuario
                venta.detalles  # cargar relación detalles con productos
            return {"success": True, "data": ventas}
        except SQLAlchemyError as e:
            logger.error(f"Error en VentaService.get_all_ventas: {e}")
            return {"success": False, "message": "Error al obtener ventas"}

    def get_venta_by_id(self, db: Session, venta_id: int):
        try:
            venta = db.query(Venta).filter(Venta.id == venta_id).first()
            if not venta:
                return {"success": False, "message": "Venta no encontrada"}
            venta.usuario
            venta.detalles
            return {"success": True, "data": venta}
        except SQLAlchemyError as e:
            logger.error(f"Error en VentaService.get_venta_by_id: {e}")
            return {"success": False, "message": "Error al obtener venta"}

    def create_venta(self, db: Session, usuario_id: int, detalles: list[VentaCreate]):
        try:
            total = 0
            venta_detalles = []

            # Verificar stock y calcular subtotal
            for item in detalles:
                producto = db.query(Producto).filter(Producto.id == item.producto_id).first()
                if not producto:
                    raise Exception(f"Producto {item.producto_id} no encontrado")
                if producto.stock < item.cantidad:
                    raise Exception(f"Stock insuficiente para {producto.nombre}")

                subtotal = producto.precio * item.cantidad
                total += subtotal
                venta_detalles.append({
                    "producto_id": producto.id,
                    "cantidad": item.cantidad,
                    "precio": producto.precio,
                    "subtotal": subtotal
                })

            # Crear venta
            venta = Venta(usuario_id=usuario_id, total=total)
            db.add(venta)
            db.commit()
            db.refresh(venta)

            # Crear detalles
            for detalle in venta_detalles:
                detalle_venta = DetalleVenta(venta_id=venta.id, **detalle)
                db.add(detalle_venta)
                # Reducir stock
                producto = db.query(Producto).filter(Producto.id == detalle["producto_id"]).first()
                producto.stock -= detalle["cantidad"]

            db.commit()
            db.refresh(venta)
            return self.get_venta_by_id(db, venta.id)
        except Exception as e:
            db.rollback()
            logger.error(f"Error en VentaService.create_venta: {e}")
            return {"success": False, "message": str(e)}

    def get_ventas_por_periodo(self, db: Session, fecha_inicio, fecha_fin):
        try:
            ventas = db.query(Venta).filter(Venta.fecha.between(fecha_inicio, fecha_fin)).order_by(Venta.fecha.asc()).all()
            total_ventas = len(ventas)
            total_ingresos = sum([venta.total for venta in ventas])
            promedio_venta = round(total_ingresos / total_ventas, 2) if total_ventas > 0 else 0

            for venta in ventas:
                venta.usuario
                venta.detalles

            return {
                "success": True,
                "data": {
                    "ventas": ventas,
                    "estadisticas": {
                        "totalVentas": total_ventas,
                        "totalIngresos": total_ingresos,
                        "promedioVenta": promedio_venta
                    }
                }
            }
        except SQLAlchemyError as e:
            logger.error(f"Error en VentaService.get_ventas_por_periodo: {e}")
            return {"success": False, "message": "Error al obtener reporte de ventas"}


# Instancia única para usar en routers
venta_service = VentaService()
