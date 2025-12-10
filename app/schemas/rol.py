from pydantic import BaseModel
from typing import Optional

# Esquema base
class RolBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None  # Solo los campos que existen en la DB

# Esquema para creación
class RolCreate(RolBase):
    pass

# Esquema para actualización (todos los campos opcionales)
class RolUpdate(BaseModel):
    nombre: Optional[str]
    descripcion: Optional[str]

# Esquema de respuesta (Output)
class RolResponse(RolBase):
    id: int

    model_config = {
        "from_attributes": True  # Pydantic v2: permite mapear atributos ORM
    }
