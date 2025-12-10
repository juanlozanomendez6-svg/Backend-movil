# app/schemas/inventario.py
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from decimal import Decimal

# -------------------------------
# Historial de inventario
# -------------------------------
class InventarioHistorialBase(BaseModel):
    producto_id: int
    usuario_id: int
    cambio: int
    motivo: str
    fecha: datetime

class InventarioHistorialResponse(InventarioHistorialBase):
    id: int

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }

# -------------------------------
# Stock bajo
# -------------------------------
class StockBajoResponse(BaseModel):
    producto_id: int
    nombre_producto: str
    stock_actual: int
    stock_minimo: Optional[int] = 5  # valor por defecto

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }

# -------------------------------
# Estadísticas de inventario
# -------------------------------
class InventarioEstadisticasResponse(BaseModel):
    total_productos: int
    productos_con_stock_bajo: int
    productos_sin_stock: int
    valor_total_inventario: Decimal

    # Configuración Pydantic v2
    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
        "alias_generator": lambda x: {
            "total_productos": "totalProductos",
            "productos_con_stock_bajo": "productosStockBajo",
            "productos_sin_stock": "productosSinStock",
            "valor_total_inventario": "valorTotalInventario"
        }[x]
    }
