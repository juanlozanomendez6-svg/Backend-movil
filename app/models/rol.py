# app/models/rol.py
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.config.db import Base

class Rol(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)

    # Relaciones
    usuarios = relationship("Usuario", back_populates="rol")
