# app/controllers/inventario_controller.py
from sqlalchemy.orm import Session
from app.services.inventario_service import inventario_service
from app.schemas.inventario import (
    InventarioHistorialResponse,
    StockBajoResponse,
    InventarioEstadisticasResponse
)

# -------------------------------
# Historial de inventario
# -------------------------------
def get_inventory_history(db: Session, producto_id: int = None, fecha_inicio=None, fecha_fin=None):
    data = inventario_service.get_inventory_history(db, producto_id, fecha_inicio, fecha_fin)["data"]
    # Mapear a Pydantic
    return [InventarioHistorialResponse.from_orm(d) for d in data]

# -------------------------------
# Registrar movimiento
# -------------------------------
def register_inventory_movement(db: Session, producto_id: int, usuario_id: int, cambio: int, motivo: str):
    movimiento = inventario_service.register_movement(db, producto_id, usuario_id, cambio, motivo)["data"]
    return InventarioHistorialResponse.from_orm(movimiento)

# -------------------------------
# Stock bajo
# -------------------------------
def get_low_stock(db: Session, umbral: int = 10):
    productos = inventario_service.get_low_stock(db, umbral)["data"]
    # Mapear a StockBajoResponse
    return [
        StockBajoResponse(
            producto_id=p.id,
            nombre_producto=p.nombre,
            stock_actual=p.stock,
            stock_minimo=umbral
        )
        for p in productos
    ]

# -------------------------------
# Estadísticas de inventario
# -------------------------------
def get_inventory_statistics(db: Session):
    stats = inventario_service.get_inventory_statistics(db)["data"]
    # Mapear a Pydantic
    return InventarioEstadisticasResponse(
        total_productos=stats["total_productos"],
        productos_con_stock_bajo=stats["productos_con_stock_bajo"],
        productos_sin_stock=stats["productos_sin_stock"],
        valor_total_inventario=stats["valor_total_inventario"]
    )
