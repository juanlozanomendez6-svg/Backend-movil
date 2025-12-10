from pydantic import BaseModel
from decimal import Decimal

class DetalleVentaBase(BaseModel):
    venta_id: int
    producto_id: int
    cantidad: int
    precio: Decimal
    subtotal: Decimal

class DetalleVentaCreate(DetalleVentaBase):
    pass

class DetalleVentaResponse(DetalleVentaBase):
    id: int

    class Config:
        orm_mode = True  # permite convertir objetos ORM a Pydantic
