from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProductoImagenBase(BaseModel):
    producto_id: int
    url: str
    descripcion: Optional[str] = None

class ProductoImagenCreate(ProductoImagenBase):
    pass

class ProductoImagenUpdate(BaseModel):
    url: Optional[str] = None
    descripcion: Optional[str] = None

class ProductoImagenResponse(ProductoImagenBase):
    id: int
    creado_en: datetime

    class Config:
        from_attributes = True
