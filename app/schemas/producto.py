from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

# Base de producto
class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: Decimal
    stock: int
    categoria_id: Optional[int]
    activo: Optional[bool] = True

# Crear producto
class ProductoCreate(ProductoBase):
    pass

# Actualizar producto (todos los campos opcionales)
class ProductoUpdate(BaseModel):
    nombre: Optional[str]
    descripcion: Optional[str]
    precio: Optional[Decimal]
    stock: Optional[int]
    categoria_id: Optional[int]
    activo: Optional[bool]

# Respuesta de producto (salida de la API)
class ProductoResponse(ProductoBase):
    id: int

    model_config = {
        "from_attributes": True  # Pydantic v2: permite usar atributos ORM
    }

# Actualizar solo stock
class StockUpdate(BaseModel):
    stock: int
