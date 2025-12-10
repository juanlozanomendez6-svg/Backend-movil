from pydantic import BaseModel
from typing import Optional

# Base para todas las categorías
class CategoriaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    

# Schema para crear una categoría
class CategoriaCreate(CategoriaBase):
    pass

# Schema para actualizar una categoría
class CategoriaUpdate(BaseModel):
    nombre: Optional[str]
    descripcion: Optional[str]

# Schema para salida (respuesta de la API)
class CategoriaOut(CategoriaBase):
    id: int

    class Config:
        orm_mode = True  # permite convertir objetos ORM a Pydantic
