from pydantic import BaseModel
from typing import List
from decimal import Decimal

# Schema para los detalles de la venta (entrada)
class DetalleVentaCreate(BaseModel):
    producto_id: int
    cantidad: int
    precio: Decimal
    subtotal: Decimal

# Schema base para la venta
class VentaBase(BaseModel):
    usuario_id: int
    total: Decimal

# Schema para crear una venta
class VentaCreate(VentaBase):
    detalles: List[DetalleVentaCreate]  # Cada detalle validado

# Schema de respuesta de detalle de venta (salida)
class DetalleVentaResponse(DetalleVentaCreate):
    id: int

    model_config = {
        "from_attributes": True
    }

# Schema de respuesta de venta (salida)
class VentaResponse(VentaBase):
    id: int
    detalles: List[DetalleVentaResponse]

    model_config = {
        "from_attributes": True
    }
