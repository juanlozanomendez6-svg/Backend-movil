from pydantic import BaseModel, EmailStr
from typing import Optional

# Base para todos los usuarios
class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    rol_id: int
    activo: Optional[bool] = True

# Schema para crear un usuario
class UsuarioCreate(UsuarioBase):
    password: str

# Schema para actualizar un usuario (todos los campos opcionales)
class UsuarioUpdate(BaseModel):
    nombre: Optional[str]
    email: Optional[EmailStr]
    rol_id: Optional[int]
    activo: Optional[bool]

# Schema para login
class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str

# Schema para la respuesta de usuario (lo que devuelve la API)
class UsuarioOut(UsuarioBase):
    id: int

    model_config = {
        "from_attributes": True  # Pydantic v2: permite mapear objetos ORM
    }
